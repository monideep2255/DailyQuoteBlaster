import os
import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from logger import get_logger

# Initialize logger
logger = get_logger(__name__)

# Load environment variables
load_dotenv()

class Database:
    def __init__(self):
        """Initialize database connection."""
        self.conn = None
        self.connect()
        
    def connect(self):
        """Connect to PostgreSQL database."""
        try:
            # Get database connection string from environment variables
            database_url = os.environ.get("DATABASE_URL")
            if not database_url:
                logger.error("DATABASE_URL environment variable not set")
                raise ValueError("DATABASE_URL environment variable not set")
                
            self.conn = psycopg2.connect(
                database_url,
                cursor_factory=RealDictCursor
            )
            self.conn.autocommit = True
            logger.info("Database connection established")
            
            # Initialize tables if they don't exist
            self.init_tables()
        except Exception as e:
            logger.error(f"Database connection error: {e}")
            self.conn = None
            raise
    
    def init_tables(self):
        """Initialize database tables if they don't exist."""
        if not self.conn:
            logger.error("Cannot initialize tables: No database connection")
            return False
            
        try:
            with self.conn.cursor() as cur:
                # Create subscribers table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS subscribers (
                        id SERIAL PRIMARY KEY,
                        email VARCHAR(255),
                        phone VARCHAR(50),
                        morning_delivery BOOLEAN DEFAULT TRUE,
                        evening_delivery BOOLEAN DEFAULT TRUE,
                        categories TEXT[],
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        active BOOLEAN DEFAULT TRUE,
                        CONSTRAINT email_or_phone CHECK (email IS NOT NULL OR phone IS NOT NULL)
                    )
                """)
                
                # Create quotes_sent table to track quote delivery
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS quotes_sent (
                        id SERIAL PRIMARY KEY,
                        subscriber_id INTEGER REFERENCES subscribers(id),
                        quote_text TEXT NOT NULL,
                        quote_author VARCHAR(255) NOT NULL,
                        category VARCHAR(50) NOT NULL,
                        delivery_method VARCHAR(10) NOT NULL,
                        time_of_day VARCHAR(10) NOT NULL,
                        sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                logger.info("Database tables initialized")
                return True
        except Exception as e:
            logger.error(f"Error initializing tables: {e}")
            return False
    
    def add_subscriber(self, email=None, phone=None, morning=True, evening=True, categories=None):
        """
        Add a new subscriber to the database.
        
        Args:
            email: Email address (optional if phone provided)
            phone: Phone number (optional if email provided)
            morning: Whether to send morning quotes
            evening: Whether to send evening quotes
            categories: List of preferred quote categories
            
        Returns:
            int: The ID of the newly created subscriber, or None on error
        """
        if not self.conn:
            logger.error("Cannot add subscriber: No database connection")
            return None
            
        if not email and not phone:
            logger.error("Cannot add subscriber: Either email or phone must be provided")
            return None
        
        if categories is None:
            categories = ["general", "motivational", "wisdom", "growth", "decisions", "success"]
        
        try:
            with self.conn.cursor() as cur:
                query = """
                    INSERT INTO subscribers (email, phone, morning_delivery, evening_delivery, categories)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id
                """
                cur.execute(query, (email, phone, morning, evening, categories))
                result = cur.fetchone()
                subscriber_id = result.get('id') if result else None
                
                if subscriber_id:
                    logger.info(f"Added new subscriber: {email or phone}, ID: {subscriber_id}")
                    return subscriber_id
                else:
                    logger.error("Failed to add subscriber: No ID returned")
                    return None
        except Exception as e:
            logger.error(f"Error adding subscriber: {e}")
            return None
    
    def get_subscribers_for_delivery(self, time_of_day):
        """
        Get all subscribers who should receive quotes at the specified time of day.
        
        Args:
            time_of_day: Either 'morning' or 'evening'
            
        Returns:
            list: List of subscriber dictionaries
        """
        if not self.conn:
            logger.error("Cannot get subscribers: No database connection")
            return []
            
        if time_of_day not in ('morning', 'evening'):
            logger.error("Invalid time_of_day value, must be 'morning' or 'evening'")
            return []
        
        delivery_column = 'morning_delivery' if time_of_day == 'morning' else 'evening_delivery'
        
        try:
            with self.conn.cursor() as cur:
                query = sql.SQL("""
                    SELECT * FROM subscribers
                    WHERE {} = TRUE AND active = TRUE
                """).format(sql.Identifier(delivery_column))
                
                cur.execute(query)
                subscribers = cur.fetchall()
                logger.info(f"Found {len(subscribers)} subscribers for {time_of_day} delivery")
                return subscribers
        except Exception as e:
            logger.error(f"Error getting subscribers for {time_of_day} delivery: {e}")
            return []
    
    def record_quote_sent(self, subscriber_id, quote_text, quote_author, category, 
                          delivery_method, time_of_day):
        """
        Record a quote that was sent to a subscriber.
        
        Args:
            subscriber_id: ID of the subscriber
            quote_text: The text of the quote
            quote_author: The author of the quote
            category: The category of the quote
            delivery_method: Either 'email' or 'sms'
            time_of_day: Either 'morning' or 'evening'
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.conn:
            logger.error("Cannot record quote: No database connection")
            return False
            
        try:
            with self.conn.cursor() as cur:
                query = """
                    INSERT INTO quotes_sent 
                    (subscriber_id, quote_text, quote_author, category, delivery_method, time_of_day)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                cur.execute(query, (
                    subscriber_id, quote_text, quote_author, category,
                    delivery_method, time_of_day
                ))
                logger.info(f"Recorded quote sent to subscriber {subscriber_id}")
                return True
        except Exception as e:
            logger.error(f"Error recording quote: {e}")
            return False
    
    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None
            logger.info("Database connection closed")

# Create a singleton instance
db = Database()