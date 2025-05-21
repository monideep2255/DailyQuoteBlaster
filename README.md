*Last Updated: May 21, 2025*

# 📧 Daily Quote Sender – Charge-Up Edition

> **✅ PHASE 1 COMPLETE!** The application now features a fully implemented Quote Randomizer and Email Sender with categorized quotes, beautiful email templates, and scheduled delivery twice daily.

A Python-based application that randomly selects and emails daily inspirational quotes to brighten your day and foster a positive mindset.

## Project Overview

### Background & Context
In our busy lives, it's beneficial to have small rituals that promote intentional living and positive thinking. The **Daily Quote Sender** provides:
- A simple automation that delivers daily inspiration
- A thoughtfully curated collection of categorized quotes
- A seamless experience that requires no user interaction
- A morning boost and evening reflection to bookend your day

### Problem Statement
- Many people want daily inspiration but don't want another app to manage
- Existing quote apps are often ad-filled or require active engagement
- People prefer simple tools that work reliably in the background

## Implemented Features

### ✨ Phase 1: Quote Randomizer + Email Sender
1. **Core Quote System**
   - Curated collection of 30+ general quotes
   - 5 specialized categories: Motivational, Wisdom, Growth, Decisions, Success
   - Intelligent category selection based on day of the week
   - Custom morning and evening delivery modes

2. **Beautiful Email Delivery**
   - Responsive HTML email templates with clean design
   - Category-specific colors and emojis for visual recognition
   - Professionally formatted quote presentation
   - Themed subject lines for morning inspiration and evening reflection

3. **Automated Scheduling**
   - Twice-daily delivery at 7 AM and 9 PM
   - Persistent running via Replit's workflow system
   - Category-specific preferences based on time of day
   - Comprehensive logging with timestamp and delivery confirmation

4. **Robust Error Handling**
   - Fallback quotes when files can't be loaded
   - Multiple layers of error recovery
   - Detailed logging for troubleshooting
   - Graceful failure management

5. **Email Service Integration**
   - Integration with Resend for reliable email delivery
   - API key management through secure environment variables
   - Delivery tracking with unique email IDs
   - Plain text alternatives for all emails

## Technical Stack

- **Language**: Python 3.9+
- **Email Service**: Resend
- **Scheduling**: Python Schedule library
- **Deployment**: Replit
- **Data Storage**: JSON files

## Environment Setup

### Required Environment Variables

The application requires certain environment variables to be set. Create a `.env` file in the root directory with the following variables:

```
# Resend API Configuration
RESEND_API_KEY=your_resend_api_key_here

# Email Configuration  
RECIPIENT_EMAIL=your-email@example.com
SENDER_EMAIL=daily-quotes@resend.dev
```

### Getting Started

1. Clone the repository
2. Create the `.env` file with required environment variables
3. Install dependencies: `pip install -r requirements.txt`
4. Start the scheduler: `python scheduler.py`

## Project Structure

```
└── Daily-Quote-Sender/
    ├── quotes.json                # Original quotes collection
    ├── quotes_categories.json     # Categorized quotes by theme
    ├── main.py                    # Core quote selection and sending logic
    ├── send_email.py              # Email template and delivery functions
    ├── scheduler.py               # Scheduling service (7AM and 9PM)
    ├── logger.py                  # Logging configuration
    ├── .env                       # Environment variables (not in repo)
    ├── .env.example               # Example environment variables
    └── README.md                  # Project documentation
```

## Future Phases

### 📱 Phase 2: SMS Support
- Integration with Twilio for SMS delivery
- User configuration for preferred delivery method
- More compact quote formatting for mobile devices

### 🌐 Phase 3: Frontend UI (Optional)
- Simple web interface to view quote history
- Subscription management
- Custom quote list uploading

## Usage Examples

```python
# Send a test quote immediately
python main.py

# Start the daily scheduler (runs at 7 AM and 9 PM)
python scheduler.py

# Run with immediate testing
RUN_IMMEDIATELY=true python scheduler.py
```
