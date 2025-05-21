import os
import sys
import resend
from datetime import datetime
from logger import get_logger

logger = get_logger(__name__)

def get_resend_key():
    """Get Resend API key from environment variables."""
    resend_key = os.environ.get('RESEND_API_KEY')
    if not resend_key:
        logger.error("RESEND_API_KEY environment variable must be set")
        sys.exit('RESEND_API_KEY environment variable must be set')
    return resend_key

def get_category_style(category):
    """
    Get the styling for a specific quote category.
    Each category has its own color scheme and styling.
    
    Args:
        category: The quote category
        
    Returns:
        tuple: (border_color, background_color, accent_color, emoji)
    """
    styles = {
        "motivational": ("#ff7b25", "#fff8f0", "#ff7b25", "🔥"),
        "wisdom": ("#4b6cb7", "#f0f8ff", "#4b6cb7", "🧠"),
        "growth": ("#2ecc71", "#f0fff0", "#27ae60", "🌱"),
        "decisions": ("#9b59b6", "#faf0ff", "#8e44ad", "⚖️"),
        "success": ("#f1c40f", "#fffdf0", "#f39c12", "🏆"),
        "general": ("#3498db", "#f9f9f9", "#3498db", "💫")
    }
    
    return styles.get(category, styles["general"])

def create_email_template(quote_text, quote_author, category="general"):
    """
    Create an HTML email template with the quote.
    
    Args:
        quote_text: The text of the quote
        quote_author: The author of the quote
        category: The category of the quote
        
    Returns:
        tuple: (html_content, plain_text)
    """
    border_color, bg_color, accent_color, emoji = get_category_style(category)
    
    # Get the current date
    current_date = datetime.now().strftime("%A, %B %d, %Y")
    
    # Create category title with proper capitalization
    category_title = category.capitalize()
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                background-color: #ffffff;
            }}
            .header {{
                text-align: center;
                margin-bottom: 20px;
            }}
            .date {{
                color: #888;
                font-size: 14px;
                margin-bottom: 5px;
            }}
            .title {{
                color: {accent_color};
                margin-top: 0;
                margin-bottom: 10px;
            }}
            .category-badge {{
                display: inline-block;
                background-color: {accent_color};
                color: white;
                padding: 5px 12px;
                border-radius: 20px;
                font-size: 14px;
                margin-bottom: 20px;
            }}
            .quote-container {{
                padding: 30px;
                background-color: {bg_color};
                border-left: 4px solid {border_color};
                border-radius: 4px;
                margin: 20px 0;
                box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            }}
            .quote-text {{
                font-size: 20px;
                font-style: italic;
                margin-bottom: 15px;
                line-height: 1.4;
            }}
            .quote-author {{
                font-weight: bold;
                text-align: right;
                color: #555;
            }}
            .emoji {{
                font-size: 24px;
                margin-right: 8px;
                vertical-align: middle;
            }}
            .footer {{
                margin-top: 30px;
                padding-top: 20px;
                border-top: 1px solid #eee;
                font-size: 12px;
                color: #777;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <div class="date">{current_date}</div>
            <h2 class="title">Your Daily Inspiration</h2>
            <div class="category-badge"><span class="emoji">{emoji}</span>{category_title}</div>
        </div>
        
        <div class="quote-container">
            <div class="quote-text">"{quote_text}"</div>
            <div class="quote-author">— {quote_author}</div>
        </div>
        
        <div class="footer">
            <p>Start your day with a positive mindset!</p>
            <p>Daily Quote Sender – Charge-Up Edition</p>
        </div>
    </body>
    </html>
    """
    
    plain_text = f"""
Your Daily Inspiration - {category_title} {emoji}
{current_date}

"{quote_text}"
— {quote_author}

Start your day with a positive mindset!
Daily Quote Sender – Charge-Up Edition
    """
    
    return html_content, plain_text

def send_quote_email(to_email, from_email, quote_text, quote_author, category="general", subject=None):
    """
    Send an email with the quote of the day.
    
    Args:
        to_email: Recipient email address
        from_email: Sender email address
        quote_text: The quote text
        quote_author: The quote author
        category: The quote category (default: "general")
        subject: Email subject (optional)
        
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        resend_key = get_resend_key()
        
        # Initialize Resend with the API key
        resend.api_key = resend_key
        
        # Get category emoji for subject line
        _, _, _, emoji = get_category_style(category)
        
        # Set subject line with category and emoji if not provided
        if subject is None:
            category_name = category.capitalize()
            subject = f"Your Daily {category_name} Quote {emoji} | Charge-Up Edition"
        
        html_content, plain_text = create_email_template(quote_text, quote_author, category)
        
        # Send the email with Resend
        response = resend.Emails.send({
            "from": f"Daily Quote <{from_email}>",
            "to": to_email,
            "subject": subject,
            "html": html_content,
            "text": plain_text,
            "tags": [
                {
                    "name": "category",
                    "value": category
                }
            ]
        })
        
        logger.info(f"Email sent successfully with Resend! ID: {response['id']}")
        return True
    except Exception as e:
        logger.error(f"Resend error: {e}")
        return False
        
def test_email_delivery(recipient_email):
    """
    Test email delivery with a test message.
    
    Args:
        recipient_email: Recipient email address
        
    Returns:
        bool: True if test email sent successfully, False otherwise
    """
    try:
        test_quote = {
            "text": "This is a test quote to verify email delivery.",
            "author": "Daily Quote Sender"
        }
        
        result = send_quote_email(
            to_email=recipient_email,
            from_email="daily-quotes@resend.dev",
            quote_text=test_quote["text"],
            quote_author=test_quote["author"],
            subject="[TEST] Daily Quote Sender - Test Email"
        )
        
        return result
    except Exception as e:
        logger.error(f"Test email delivery error: {e}")
        return False
