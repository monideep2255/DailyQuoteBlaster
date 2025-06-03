*Last Updated: May 23, 2025*

# 📧 Daily Quote Sender – Charge-Up Edition

> **✅ ALL PHASES COMPLETE!** The application now features a fully implemented Quote Randomizer with Email and SMS delivery, beautiful templates, database integration, web interface, and scheduled delivery twice daily.

A full-stack application that sends motivational quotes via email and SMS, with a responsive web interface for quote viewing and subscription management.

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

### ✨ Phase 1: Quote Randomizer + Email Sender ✓ COMPLETE
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

### 📱 Phase 2: SMS Support + Database Integration ✓ COMPLETE
1. **SMS Delivery System**
   - Integration with Twilio for SMS delivery
   - Compact SMS templates optimized for mobile
   - Category-specific SMS formatting
   - Delivery confirmation and logging

2. **Database Integration**
   - PostgreSQL database for subscriber management
   - Subscriber preferences storage (email/SMS/time/categories)
   - Quote delivery tracking and history
   - Efficient query optimization for subscriber filtering

3. **Subscriber Management**
   - Add new subscribers via API or web interface
   - Configure delivery preferences (email, SMS, or both)
   - Morning and evening delivery options
   - Category preferences for personalized content

4. **Multi-Channel Support**
   - Ability to receive quotes via email, SMS, or both
   - Channel-specific formatting and presentation
   - Unified subscriber management across channels
   - Consistent quote selection logic regardless of channel

### 🌐 Phase 3: Web Interface + Public Deployment ✓ COMPLETE
1. **Responsive Web Interface**
   - Modern, responsive design with clean aesthetics
   - Mobile-friendly layout and controls
   - Category-based filtering system
   - Recent quotes display with timestamps

2. **Subscription Management**
   - User-friendly subscription form
   - Email and SMS subscription options
   - Delivery time preference selection
   - Category selection for personalized content

3. **Quote Archive**
   - View recently sent quotes
   - Filter quotes by category
   - Refresh functionality for new quotes
   - Professionally styled quote cards

4. **Public Hosting**
   - Node.js express server for the web interface
   - RESTful API endpoints for subscription and quote retrieval
   - Complete deployment instructions for Netlify
   - Environment variable management for secure deployment

## Technical Stack

### Backend
- **Primary Language**: Python 3.9+
- **Secondary Language**: Node.js (web server)
- **Email Services**: 
  - Resend API (primary)
  - SendGrid API (optional alternative)
- **SMS Service**: Twilio API
- **Scheduling**: Python Schedule library
- **Database**: PostgreSQL
- **Static Data**: JSON files for quotes

### Frontend
- **HTML/CSS/JavaScript**: Responsive web interface
- **CSS Framework**: Tailwind CSS for styling
- **Icons**: Font Awesome
- **Responsive Design**: Mobile-first approach

### Deployment
- **Backend Hosting**: Replit
- **Database**: PostgreSQL on Replit
- **Frontend Hosting**: Options include Netlify, Vercel, or GitHub Pages

## Environment Setup

### Required Environment Variables

The application requires certain environment variables to be set. Create a `.env` file in the root directory with the following variables:

```
# Database Configuration
DATABASE_URL=postgresql://username:password@host:port/database

# Email Services (choose one)
RESEND_API_KEY=your_resend_api_key_here
# or
SENDGRID_API_KEY=your_sendgrid_api_key_here

# SMS Service
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number

# Email Configuration  
SENDER_EMAIL=daily-quotes@yourdomain.com
```

### Getting Started

1. Clone the repository
2. Create the `.env` file with required environment variables
3. Install dependencies:
   ```
   pip install -r requirements.txt
   npm install
   ```
4. Set up the database:
   ```
   psql -U postgres -c "CREATE DATABASE daily_quotes;"
   ```
5. Start the scheduler and web server:
   ```
   python scheduler.py
   node server.js
   ```

## Project Structure

```
└── Daily-Quote-Sender/
    ├── backend/                  # Backend API endpoints
    ├── frontend/                 # Frontend web interface
    │   ├── index.html           # Main HTML page
    │   ├── styles.css           # CSS styles
    │   └── scripts.js           # JavaScript functionality
    ├── quotes.json              # Original quotes collection
    ├── quotes_categories.json   # Categorized quotes by theme
    ├── main.py                  # Core quote selection logic
    ├── scheduler.py             # Scheduling service (7AM and 9PM)
    ├── send_email.py            # Email template and delivery functions
    ├── send_sms.py              # SMS delivery functions
    ├── database.py              # Database connection and queries
    ├── add_subscriber.py        # Subscriber management function
    ├── get_recent_quotes.py     # Recent quotes retrieval
    ├── server.js                # Node.js Express web server
    ├── logger.py                # Logging configuration
    ├── .env                     # Environment variables (not in repo)
    ├── .env.example             # Example environment variables
    └── README.md                # Project documentation
```

## Deployment Instructions

### Backend Deployment on Replit

1. Create a new Replit project
2. Upload all files or connect to your GitHub repository
3. Configure the Secrets (environment variables) in the Replit project
4. Use the "Deployments" feature to deploy your project

### Frontend Deployment on Netlify

1. Create a free Netlify account at [netlify.com](https://www.netlify.com/)
2. From the Netlify dashboard, click "New site from Git"
3. Connect to your GitHub repository
4. Configure the build settings:
   - Build command: `npm run build` (if using a build process)
   - Publish directory: `frontend` (or the directory containing your static files)
5. Configure environment variables in the Netlify UI:
   - Go to Site settings > Build & deploy > Environment
   - Add the same environment variables you used locally
6. Deploy your site and enjoy your public Daily Quote Sender!

## Usage Examples

```bash
# Start the scheduler (runs at 7 AM and 9 PM)
python scheduler.py

# Start the web server
node server.js

# Send a test email
python send_email.py test@example.com

# Send a test SMS
python send_sms.py +1234567890

# Add a new subscriber (email or phone is sufficient)
python add_subscriber.py user@example.com
# Or using a phone number only
python add_subscriber.py "" +1234567890

# View recent quotes
python get_recent_quotes.py
```
