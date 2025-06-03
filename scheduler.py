#!/usr/bin/env python3
import os
import time
import schedule
import json
import random
from datetime import datetime
from dotenv import load_dotenv
from logger import get_logger
from database import db
from send_email import send_quote_email
from send_sms import send_quote_sms

# Initialize logger
logger = get_logger(__name__)

# Load environment variables
load_dotenv()

def load_quotes(quotes_file='quotes.json', categories_file='quotes_categories.json'):
    """
    Load quotes from JSON files.
    
    Args:
        quotes_file: Path to the original quotes file
        categories_file: Path to the categorized quotes file
    
    Returns:
        dict: A dictionary with all quotes organized by category
    """
    all_quotes = {
        "general": []
    }
    
    # Load original quotes file
    try:
        with open(quotes_file, 'r') as f:
            data = json.load(f)
            all_quotes["general"] = data.get('quotes', [])
            logger.info(f"Loaded {len(all_quotes['general'])} quotes from {quotes_file}")
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.warning(f"Error loading original quotes file: {e}")
        all_quotes["general"] = [
            {"text": "The best way to predict the future is to create it.", "author": "Abraham Lincoln"},
            {"text": "Believe you can and you're halfway there.", "author": "Theodore Roosevelt"}
        ]
    
    # Load categorized quotes
    try:
        with open(categories_file, 'r') as f:
            categories_data = json.load(f)
            # Merge categorized quotes into all_quotes
            for category, quotes in categories_data.items():
                all_quotes[category] = quotes
            
            logger.info(f"Loaded categorized quotes from {categories_file} with {len(categories_data)} categories")
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.warning(f"Error loading categorized quotes file: {e}, continuing with general quotes only")
    
    # Validate we have at least some quotes
    if not any(all_quotes.values()):
        logger.error("No quotes found in any category. Using fallback quotes.")
        all_quotes["general"] = [
            {"text": "Every day is a new beginning.", "author": "Unknown"},
            {"text": "The journey of a thousand miles begins with a single step.", "author": "Lao Tzu"}
        ]
    
    return all_quotes

def select_random_quote(quotes_dict, preferred_category=None):
    """
    Select a random quote, optionally from a preferred category.
    
    Args:
        quotes_dict: Dictionary of quotes by category
        preferred_category: Optional category to prefer (if it exists and has quotes)
    
    Returns:
        dict: A quote object with text, author, and category
    """
    available_categories = [cat for cat, quotes in quotes_dict.items() if quotes]
    
    if not available_categories:
        logger.error("No quotes available in any category")
        return {
            "text": "Every day is a new beginning.",
            "author": "Unknown",
            "category": "fallback"
        }
    
    # If preferred category exists and has quotes, use it with 75% probability
    if preferred_category and preferred_category in available_categories and random.random() < 0.75:
        selected_category = preferred_category
    else:
        # Otherwise select a random category
        selected_category = random.choice(available_categories)
    
    # Select a random quote from the chosen category
    # Copy the quote so we don't mutate the original data structure
    selected_quote = random.choice(quotes_dict[selected_category]).copy()
    selected_quote["category"] = selected_category

    return selected_quote

def determine_preferred_category(time_of_day="morning"):
    """
    Determine preferred category based on day of week and time of day.
    
    Args:
        time_of_day: Either 'morning' or 'evening'
    
    Returns:
        str: Preferred category name or None
    """
    # Get the current day of the week (0 = Monday, 6 = Sunday)
    day_of_week = datetime.now().weekday()
    
    # Different category preferences for morning and evening
    if time_of_day == "morning":
        # Morning categories - more motivational and action-oriented
        day_category_map = {
            0: "motivational",  # Monday - Motivational
            1: "growth",        # Tuesday - Growth
            2: "wisdom",        # Wednesday - Wisdom 
            3: "decisions",     # Thursday - Decisions
            4: "success",       # Friday - Success
            5: "motivational",  # Saturday - Motivational
            6: "growth"         # Sunday - Growth
        }
    else:
        # Evening categories - more reflective and wisdom-oriented
        day_category_map = {
            0: "wisdom",        # Monday - Wisdom
            1: "decisions",     # Tuesday - Decisions
            2: "growth",        # Wednesday - Growth
            3: "wisdom",        # Thursday - Wisdom
            4: "success",       # Friday - Success
            5: "wisdom",        # Saturday - Wisdom
            6: "wisdom"         # Sunday - Wisdom
        }
    
    return day_category_map.get(day_of_week)

def send_quotes(time_of_day="morning"):
    """
    Send quotes to all subscribers (email and SMS) for the specified time of day.
    
    Args:
        time_of_day: Either 'morning' or 'evening'
        
    Returns:
        bool: True if quotes were sent successfully, False otherwise
    """
    logger.info(f"Sending {time_of_day} quotes to subscribers")
    
    # Load all quotes
    all_quotes = load_quotes()
    
    # Determine preferred category based on day of week and time of day
    preferred_category = determine_preferred_category(time_of_day)
    logger.info(f"Today's preferred quote category for {time_of_day}: {preferred_category}")
    
    # Select a random quote with preference to the daily category
    quote = select_random_quote(all_quotes, preferred_category)
    logger.info(f"Selected {quote['category']} quote: '{quote['text']}' - {quote['author']}")
    
    # Create custom subject for emails based on time of day
    subject = None
    if time_of_day == "morning":
        subject = f"Your Morning Inspiration | Charge-Up Edition"
    elif time_of_day == "evening":
        subject = f"Your Evening Reflection | Charge-Up Edition"
    
    # Get subscribers for this time of day
    subscribers = db.get_subscribers_for_delivery(time_of_day)
    
    if not subscribers:
        logger.warning(f"No subscribers found for {time_of_day} delivery")
        return False
    
    success_count = 0
    
    # Process each subscriber
    for subscriber in subscribers:
        # Get subscriber details
        subscriber_id = subscriber.get('id')
        email = subscriber.get('email')
        phone = subscriber.get('phone')
        
        # Send via email if email is provided
        if email:
            try:
                email_success = send_quote_email(
                    to_email=email,
                    from_email=os.environ.get('SENDER_EMAIL', 'daily-quotes@resend.dev'),
                    quote_text=quote['text'],
                    quote_author=quote['author'],
                    category=quote.get('category', 'general'),
                    subject=subject
                )
                
                if email_success:
                    logger.info(f"Email successfully sent to subscriber {subscriber_id} ({email})")
                    db.record_quote_sent(
                        subscriber_id=subscriber_id,
                        quote_text=quote['text'],
                        quote_author=quote['author'],
                        category=quote['category'],
                        delivery_method='email',
                        time_of_day=time_of_day
                    )
                    success_count += 1
                else:
                    logger.error(f"Failed to send email to subscriber {subscriber_id} ({email})")
            except Exception as e:
                logger.error(f"Exception when sending email to {email}: {e}")
        
        # Send via SMS if phone is provided
        if phone:
            try:
                sms_success = send_quote_sms(
                    to_number=phone,
                    quote_text=quote['text'],
                    quote_author=quote['author'],
                    category=quote.get('category', 'general')
                )
                
                if sms_success:
                    logger.info(f"SMS successfully sent to subscriber {subscriber_id} ({phone})")
                    db.record_quote_sent(
                        subscriber_id=subscriber_id,
                        quote_text=quote['text'],
                        quote_author=quote['author'],
                        category=quote['category'],
                        delivery_method='sms',
                        time_of_day=time_of_day
                    )
                    success_count += 1
                else:
                    logger.error(f"Failed to send SMS to subscriber {subscriber_id} ({phone})")
            except Exception as e:
                logger.error(f"Exception when sending SMS to {phone}: {e}")
    
    logger.info(f"Completed {time_of_day} quote delivery: {success_count} successful out of {len(subscribers)} subscribers")
    return success_count > 0

def send_morning_quotes():
    """Send morning quotes at 7 AM."""
    return send_quotes(time_of_day="morning")

def send_evening_quotes():
    """Send evening quotes at 9 PM."""
    return send_quotes(time_of_day="evening")

def main():
    """Set up the scheduler to run twice a day - 7 AM and 9 PM."""
    logger.info("Starting Daily Quote Sender scheduler")
    
    # Schedule the jobs to run daily
    schedule.every().day.at("07:00").do(send_morning_quotes)
    schedule.every().day.at("21:00").do(send_evening_quotes)
    
    # Run once immediately when starting (for testing)
    if os.environ.get('RUN_IMMEDIATELY', 'false').lower() == 'true':
        logger.info("Running immediately for testing")
        time_of_day = os.environ.get('TEST_TIME_OF_DAY', 'morning')
        if time_of_day == 'morning':
            send_morning_quotes()
        else:
            send_evening_quotes()
    
    # Keep the script running indefinitely
    logger.info("Scheduler running, waiting for next scheduled time (7 AM and 9 PM daily)...")
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    main()