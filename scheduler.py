#!/usr/bin/env python3
import os
import time
import schedule
import subprocess
from datetime import datetime
from logger import get_logger

# Initialize logger
logger = get_logger(__name__)

def send_daily_quote(time_of_day="morning"):
    """
    Run the main.py script to send the daily quote.
    
    Args:
        time_of_day: Specify "morning" or "evening" to customize the email subject
    """
    logger.info(f"Scheduler triggered at {datetime.now()} for {time_of_day} quote")
    try:
        # Add environment variable to indicate time of day for the email
        env = os.environ.copy()
        env["TIME_OF_DAY"] = time_of_day
        
        # Run the main.py script as a subprocess
        process = subprocess.run(
            ["python", "main.py"], 
            capture_output=True, 
            text=True, 
            check=True,
            env=env
        )
        logger.info(f"{time_of_day.capitalize()} quote sender executed successfully: {process.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to execute {time_of_day} quote sender: {e}")
        logger.error(f"Error output: {e.stderr}")
        return False

def send_morning_quote():
    """Send the morning quote at 7 AM."""
    return send_daily_quote(time_of_day="morning")

def send_evening_quote():
    """Send the evening quote at 9 PM."""
    return send_daily_quote(time_of_day="evening")

def main():
    """Set up the scheduler to run twice a day - 7 AM and 9 PM."""
    logger.info("Starting Daily Quote Sender scheduler")
    
    # Schedule the jobs to run daily
    schedule.every().day.at("07:00").do(send_morning_quote)
    schedule.every().day.at("21:00").do(send_evening_quote)
    
    # Run once immediately when starting (for testing)
    if os.environ.get('RUN_IMMEDIATELY', 'false').lower() == 'true':
        logger.info("Running immediately for testing")
        send_morning_quote()
    
    # Keep the script running indefinitely
    logger.info("Scheduler running, waiting for next scheduled time (7 AM and 9 PM daily)...")
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    main()