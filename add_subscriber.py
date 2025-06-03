#!/usr/bin/env python3
import sys
import json
from database import db
from logger import get_logger

logger = get_logger(__name__)

def add_subscriber(email=None, phone=None, morning=True, evening=True, categories=None):
    """
    Add a new subscriber to the database.
    
    Args:
        email: Email address (optional if phone provided)
        phone: Phone number (optional if email provided)
        morning: Whether to send morning quotes (True/False)
        evening: Whether to send evening quotes (True/False)
        categories: Comma-separated list of preferred quote categories
        
    Returns:
        dict: Result with success status and subscriber ID
    """
    try:
        if not email and not phone:
            logger.error("Cannot add subscriber: Either email or phone must be provided")
            return {"success": False, "message": "Either email or phone must be provided"}
            
        # Convert string values to appropriate types
        morning_bool = morning.lower() == 'true' if isinstance(morning, str) else bool(morning)
        evening_bool = evening.lower() == 'true' if isinstance(evening, str) else bool(evening)
        
        # Process categories
        if categories:
            if isinstance(categories, str):
                category_list = categories.split(',')
            else:
                category_list = categories
                
            # If "all" is selected, include all categories
            if "all" in category_list:
                category_list = ["general", "motivational", "wisdom", "growth", "decisions", "success"]
        else:
            category_list = ["general", "motivational", "wisdom", "growth", "decisions", "success"]
            
        # Add subscriber to database
        subscriber_id = db.add_subscriber(
            email=email if email else None,
            phone=phone if phone else None,
            morning=morning_bool,
            evening=evening_bool,
            categories=category_list
        )
        
        if subscriber_id:
            logger.info(f"Added new subscriber with ID {subscriber_id}")
            return {"success": True, "id": subscriber_id}
        else:
            logger.error("Failed to add subscriber")
            return {"success": False, "message": "Failed to add subscriber to database"}
            
    except Exception as e:
        logger.error(f"Error adding subscriber: {e}")
        return {"success": False, "message": str(e)}

if __name__ == "__main__":
    # This script is meant to be called from Node.js
    if len(sys.argv) < 2:
        usage_msg = (
            "Usage: python add_subscriber.py <email> <phone> [morning] "
            "[evening] [categories] - either email or phone is required"
        )
        print(json.dumps({"success": False, "message": usage_msg}))
        sys.exit(1)
        
    # Get arguments
    email = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] != '' else None
    phone = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] != '' else None
    morning = sys.argv[3] if len(sys.argv) > 3 else 'true'
    evening = sys.argv[4] if len(sys.argv) > 4 else 'true'
    categories = sys.argv[5] if len(sys.argv) > 5 else None
    
    # Add subscriber
    result = add_subscriber(email, phone, morning, evening, categories)
    
    # Return result as JSON
    print(json.dumps(result))
    sys.exit(0 if result["success"] else 1)