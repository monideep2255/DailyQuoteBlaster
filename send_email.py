import os
import sys
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from logger import get_logger

logger = get_logger(__name__)

def get_sendgrid_key():
    """Get SendGrid API key from environment variables."""
    sendgrid_key = os.environ.get('SENDGRID_API_KEY')
    if not sendgrid_key:
        logger.error("SENDGRID_API_KEY environment variable must be set")
        sys.exit('SENDGRID_API_KEY environment variable must be set')
    return sendgrid_key

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
    sendgrid_key = get_sendgrid_key()
    
    html_content, plain_text = create_email_template(quote_text, quote_author)
    
    message = Mail(
        from_email=Email(from_email),
        to_emails=To(to_email),
        subject=subject
    )
    
    # Add both HTML and plain text content
    message.content = Content("text/html", html_content)
    
    try:
        sg = SendGridAPIClient(sendgrid_key)
        response = sg.send(message)
        logger.info(f"Email sent successfully! Status code: {response.status_code}")
        return True
    except Exception as e:
        logger.error(f"SendGrid error: {e}")
        return False
