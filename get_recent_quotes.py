#!/usr/bin/env python3
import json
import sys
from database import db
from logger import get_logger

logger = get_logger(__name__)

def get_recent_quotes(limit=10):
    """
    Fetch the most recent quotes sent from the database.
    
    Args:
        limit: Maximum number of quotes to return
        
    Returns:
        list: List of quotes with text, author, date and category
    """
    try:
        with db.conn.cursor() as cur:
            query = """
                SELECT 
                    quote_text as text, 
                    quote_author as author, 
                    category,
                    sent_at::date as date
                FROM quotes_sent
                ORDER BY sent_at DESC
                LIMIT %s
            """
            cur.execute(query, (limit,))
            quotes = cur.fetchall()
            
            # Convert database records to list of dicts
            result = []
            for quote in quotes:
                result.append({
                    'text': quote['text'],
                    'author': quote['author'],
                    'category': quote['category'],
                    'date': quote['date'].isoformat() if quote['date'] else None
                })
            
            logger.info(f"Retrieved {len(result)} recent quotes from database")
            return result
    except Exception as e:
        logger.error(f"Error fetching recent quotes: {e}")
        return []

if __name__ == "__main__":
    # This script is meant to be called from Node.js and return JSON
    quotes = get_recent_quotes()
    print(json.dumps(quotes))
    sys.exit(0)