#!/usr/bin/env python3
import json
import random
import os
from dotenv import load_dotenv
from send_email import send_quote_email
from logger import get_logger

# Initialize logger
logger = get_logger(__name__)

def load_quotes(quotes_file='quotes.json'):
    """Load quotes from a JSON file."""
    try:
        with open(quotes_file, 'r') as f:
            data = json.load(f)
            return data.get('quotes', [])
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Error loading quotes file: {e}")
        # Return default fallback quotes if file not found or invalid
        return [
            {"text": "The best way to predict the future is to create it.", "author": "Abraham Lincoln"},
            {"text": "Believe you can and you're halfway there.", "author": "Theodore Roosevelt"}
        ]

def select_random_quote(quotes):
    """Select a random quote from the list."""
    if not quotes:
        logger.warning("Quote list is empty, using fallback quote")
        return {
            "text": "Every day is a new beginning.",
            "author": "Unknown"
        }
    return random.choice(quotes)

def main():
    """Main function to send daily quote."""
    # Load environment variables
    load_dotenv()
    
    # Get configuration from environment variables
    recipient_email = os.environ.get('RECIPIENT_EMAIL')
    sender_email = os.environ.get('SENDER_EMAIL', 'daily-quotes@example.com')
    
    if not recipient_email:
        logger.error("RECIPIENT_EMAIL environment variable must be set")
        return False
    
    logger.info("Starting Daily Quote Sender")
    
    # Load quotes and select a random one
    quotes = load_quotes()
    quote = select_random_quote(quotes)
    
    logger.info(f"Selected quote: '{quote['text']}' - {quote['author']}")
    
    # Send the email
    success = send_quote_email(
        to_email=recipient_email,
        from_email=sender_email,
        quote_text=quote['text'],
        quote_author=quote['author']
    )
    
    if success:
        logger.info(f"Quote successfully sent to {recipient_email}")
    else:
        logger.error(f"Failed to send quote to {recipient_email}")
    
    return success

if __name__ == "__main__":
    main()
