import pymongo
import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

def connect_to_db():
    """
    Connects to the MongoDB database.
    
    Returns:
    - collection: The MongoDB collection object.
    """
    try:
        MONGO_URI = os.getenv("MONGO_URI")
        client = pymongo.MongoClient(MONGO_URI)
        db = client['pib']
        return db['press_releases']
    except pymongo.errors.ConnectionError as e:
        logger.error(f"Database connection failed: {e}")
        return None

def store_in_db(data):
    """
    Stores the scraped data into MongoDB.
    If a document with the same URL exists, it updates it; otherwise, inserts a new document.
    """
    try:
        collection = connect_to_db()
        if isinstance(data, dict):
            result = collection.update_one(
                {'url': data['url']},
                {'$set': data},
                upsert=True
            )
            if result.upserted_id:
                logger.info(f"Inserted new document with URL: {data['url']}")
            else:
                logger.info(f"Updated existing document with URL: {data['url']}")
        elif isinstance(data, list):
            for item in data:
                collection.update_one(
                    {'url': item['url']},
                    {'$set': item},
                    upsert=True
                )
            logger.info(f"Inserted/Updated {len(data)} documents.")
        else:
            logger.error("Data must be a dict or list of dicts.")
    except Exception as e:
        logger.error(f"Error storing data to MongoDB: {e}")
        raise e