# 📧 Daily Quote Sender – Charge-Up Edition

A simple application that sends a daily motivational quote via email to start your day with a positive mindset.

## 📝 Overview

The Daily Quote Sender is a backend-driven, schedule-based tool that randomly selects a quote from a local list and sends it to a recipient via email every morning. It's designed to be:

- Minimal
- Reliable
- Automatic
- Inspirational

## 🚀 Features

- Randomly selects quotes from a predefined list
- Sends beautifully formatted emails using SendGrid
- Runs automatically via Replit's scheduler (cron job)
- Simple logging for tracking deliveries
- Fallback quotes in case of file reading errors

## 🔧 Setup & Installation

### Prerequisites

- Python 3.7+
- SendGrid account with API key

### Environment Variables

Create a `.env` file based on the `.env.example` template:

