#!/usr/bin/env python3
import sys
from send_sms import test_sms_delivery
from logger import get_logger

logger = get_logger("test_sms")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_sms.py <phone_number>")
        sys.exit(1)
    
    phone_number = sys.argv[1]
    print(f"Sending test SMS to {phone_number}")
    
    result = test_sms_delivery(phone_number)
    
    if result:
        print("Test SMS sent successfully!")
    else:
        print("Failed to send test SMS. Check logs for details.")