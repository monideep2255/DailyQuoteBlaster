#!/usr/bin/env python3
import json
import random
import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from send_email import send_quote_email
from logger import get_logger

# Initialize logger
logger = get_logger(__name__)

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

def determine_preferred_category():
    """
    Determine preferred category based on day of week or other factors.
    
    Returns:
        str: Preferred category name or None
    """
    # Get the current day of the week (0 = Monday, 6 = Sunday)
    day_of_week = datetime.now().weekday()
    
    # Map days to categories (just an example approach)
    day_category_map = {
        0: "motivational",  # Monday - Motivational
        1: "growth",        # Tuesday - Growth
        2: "wisdom",        # Wednesday - Wisdom 
        3: "decisions",     # Thursday - Decisions
        4: "success",       # Friday - Success
        5: "general",       # Saturday - General
        6: "general"        # Sunday - General
    }
    
    return day_category_map.get(day_of_week)

def main():
    """Main function to send daily quote."""
    # Load environment variables
    load_dotenv()
    
    # Get configuration from environment variables
    recipient_email = os.environ.get('RECIPIENT_EMAIL')
    sender_email = os.environ.get('SENDER_EMAIL', 'daily-quotes@resend.dev')
    time_of_day = os.environ.get('TIME_OF_DAY', 'morning')  # Default to morning if not specified
    
    if not recipient_email:
        logger.error("RECIPIENT_EMAIL environment variable must be set")
        sys.exit("RECIPIENT_EMAIL environment variable must be set")
    
    logger.info(f"Starting Daily Quote Sender - {time_of_day.capitalize()} Edition")
    
    try:
        # Load all quotes
        all_quotes = load_quotes()
        
        # Determine preferred category based on day of week
        preferred_category = determine_preferred_category()
        logger.info(f"Today's preferred quote category: {preferred_category}")
        
        # For evening quotes, we'll use a slightly different category preference
        if time_of_day.lower() == 'evening':
            # In evening, prefer wisdom and growth quotes
            evening_categories = ['wisdom', 'growth']
            if any(cat in all_quotes for cat in evening_categories):
                # Pick one of the evening categories randomly
                available_evening = [cat for cat in evening_categories if cat in all_quotes]
                preferred_category = random.choice(available_evening)
                logger.info(f"Evening quote, switched to category: {preferred_category}")
        
        # Select a random quote with preference to the appropriate category
        quote = select_random_quote(all_quotes, preferred_category)
        
        logger.info(f"Selected {quote['category']} quote: '{quote['text']}' - {quote['author']}")
        
        # Create a custom subject based on time of day
        subject = None
        if time_of_day.lower() == 'morning':
            subject = f"Your Morning Inspiration | Charge-Up Edition"
        elif time_of_day.lower() == 'evening':
            subject = f"Your Evening Reflection | Charge-Up Edition"
        
        # Send the email
        success = send_quote_email(
            to_email=recipient_email,
            from_email=sender_email,
            quote_text=quote['text'],
            quote_author=quote['author'],
            category=quote.get('category', 'general'),
            subject=subject
        )
        
        if success:
            logger.info(f"{time_of_day.capitalize()} quote successfully sent to {recipient_email}")
        else:
            logger.error(f"Failed to send {time_of_day} quote to {recipient_email}")
        
        return success
    
    except Exception as e:
        logger.error(f"Unexpected error in main: {e}")
        return False

if __name__ == "__main__":
    main()
