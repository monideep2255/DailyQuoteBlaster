#!/usr/bin/env python3
import os
import time
import schedule
import subprocess
from datetime import datetime
from logger import get_logger

# Initialize logger
logger = get_logger(__name__)

def send_daily_quote():
    """Run the main.py script to send the daily quote."""
    logger.info(f"Scheduler triggered at {datetime.now()}")
    try:
        # Run the main.py script as a subprocess
        process = subprocess.run(
            ["python", "main.py"], 
            capture_output=True, 
            text=True, 
            check=True
        )
        logger.info(f"Quote sender executed successfully: {process.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to execute quote sender: {e}")
        logger.error(f"Error output: {e.stderr}")
        return False

def main():
    """Set up the scheduler to run every day at 7 AM."""
    logger.info("Starting Daily Quote Sender scheduler")
    
    # Schedule the job to run daily at 7:00 AM
    schedule.every().day.at("07:00").do(send_daily_quote)
    
    # Run once immediately when starting (for testing)
    if os.environ.get('RUN_IMMEDIATELY', 'false').lower() == 'true':
        logger.info("Running immediately for testing")
        send_daily_quote()
    
    # Keep the script running indefinitely
    logger.info("Scheduler running, waiting for next scheduled time...")
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    main()