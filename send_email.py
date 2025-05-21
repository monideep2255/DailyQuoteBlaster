import os
import sys
import resend
from logger import get_logger

logger = get_logger(__name__)

def get_resend_key():
    """Get Resend API key from environment variables."""
    resend_key = os.environ.get('RESEND_API_KEY')
    if not resend_key:
        logger.error("RESEND_API_KEY environment variable must be set")
        sys.exit('RESEND_API_KEY environment variable must be set')
    return resend_key

def create_email_template(quote_text, quote_author):
    """Create an HTML email template with the quote."""
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .quote-container {{
                padding: 20px;
                background-color: #f9f9f9;
                border-left: 4px solid #3498db;
                margin: 20px 0;
            }}
            .quote-text {{
                font-size: 20px;
                font-style: italic;
                margin-bottom: 10px;
            }}
            .quote-author {{
                font-weight: bold;
                text-align: right;
            }}
            .footer {{
                margin-top: 30px;
                font-size: 12px;
                color: #777;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <h2>Your Daily Inspiration</h2>
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
    
    plain_text = f'"{quote_text}" — {quote_author}\n\nStart your day with a positive mindset!'
    
    return html_content, plain_text

def send_quote_email(to_email, from_email, quote_text, quote_author, subject="Your Daily Inspiration"):
    """Send an email with the quote of the day."""
    resend_key = get_resend_key()
    
    # Initialize Resend with the API key
    resend.api_key = resend_key
    
    html_content, plain_text = create_email_template(quote_text, quote_author)
    
    try:
        # Send the email with Resend
        response = resend.Emails.send({
            "from": f"Daily Quote <{from_email}>",
            "to": to_email,
            "subject": subject,
            "html": html_content,
            "text": plain_text
        })
        
        logger.info(f"Email sent successfully with Resend! ID: {response['id']}")
        return True
    except Exception as e:
        logger.error(f"Resend error: {e}")
        return False
