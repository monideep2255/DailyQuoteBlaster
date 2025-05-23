import os
import sys
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from logger import get_logger

# Initialize logger
logger = get_logger(__name__)

def get_twilio_credentials():
    """Get Twilio credentials from environment variables."""
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    from_number = os.environ.get('TWILIO_PHONE_NUMBER')
    
    if not account_sid or not auth_token or not from_number:
        logger.error("Twilio credentials not found in environment variables")
        return None, None, None
    
    return account_sid, auth_token, from_number

def create_sms_template(quote_text, quote_author, category=None):
    """
    Create an SMS template with the quote.
    
    Args:
        quote_text: The text of the quote
        quote_author: The author of the quote
        category: The category of the quote (optional)
    
    Returns:
        str: The SMS message text
    """
    # Category-specific emojis
    category_emojis = {
        "motivational": "🔥",
        "wisdom": "🧠",
        "growth": "🌱",
        "decisions": "⚖️",
        "success": "🏆",
        "general": "💫"
    }
    
    emoji = category_emojis.get(category, "💫")
    
    # Keep SMS messages concise
    sms_text = f"{emoji} Quote of the Day {emoji}\n\n\"{quote_text}\"\n— {quote_author}"
    
    # Add category if available
    if category and category != "general":
        sms_text += f"\n\n#{category.capitalize()}"
    
    sms_text += "\n\nDaily Quote Sender"
    
    return sms_text

def send_quote_sms(to_number, quote_text, quote_author, category=None):
    """
    Send an SMS with the quote of the day.
    
    Args:
        to_number: Recipient phone number
        quote_text: The text of the quote
        quote_author: The author of the quote
        category: The category of the quote (optional)
        
    Returns:
        bool: True if SMS sent successfully, False otherwise
    """
    # Get Twilio credentials
    account_sid, auth_token, from_number = get_twilio_credentials()
    
    if not account_sid or not auth_token or not from_number:
        logger.error("Cannot send SMS: Twilio credentials missing")
        return False
    
    # Check if recipient phone number is provided
    if not to_number:
        logger.error("Cannot send SMS: Recipient phone number is missing")
        return False
    
    try:
        # Create Twilio client
        client = Client(account_sid, auth_token)
        
        # Create message text
        message_text = create_sms_template(quote_text, quote_author, category)
        
        # Send SMS
        message = client.messages.create(
            body=message_text,
            from_=from_number,
            to=to_number
        )
        
        logger.info(f"SMS sent successfully! SID: {message.sid}")
        return True
    
    except TwilioRestException as e:
        logger.error(f"Twilio error: {e}")
        return False
    
    except Exception as e:
        logger.error(f"Unexpected error sending SMS: {e}")
        return False
        
def test_sms_delivery(to_number):
    """
    Test SMS delivery with a test message.
    
    Args:
        to_number: Recipient phone number
        
    Returns:
        bool: True if test SMS sent successfully, False otherwise
    """
    test_quote = {
        "text": "This is a test quote to verify SMS delivery.",
        "author": "Daily Quote Sender"
    }
    
    return send_quote_sms(
        to_number=to_number,
        quote_text=test_quote["text"],
        quote_author=test_quote["author"]
    )