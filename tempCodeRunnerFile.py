from fastapi import FastAPI, HTTPException, Query
from threading import Thread
from scrap import scrape_press_release, scrape_all_releases
from db import store_in_db
from bson import ObjectId
from datetime import datetime
from typing import Optional
import uvicorn
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="PIB Press Releases Scraper", description="An API to scrape PIB press releases.", version="1.0.0")

def convert_object_ids(data):
    """
    Converts ObjectId instances to strings for JSON serialization.
    """
    if isinstance(data, dict):
        return {k: convert_object_ids(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_object_ids(item) for item in data]
    elif isinstance(data, ObjectId):
        return str(data)
    else:
        return data

@app.get("/", tags=["Root"])
def root():
    return {"message": "Welcome to PIB Press Releases Scraper API"}

@app.get("/scrape_single", tags=["Scrape"])
def scrape_single_endpoint(url: str = Query(..., description="The URL of the press release to scrape")):
    """
    Scrapes a single press release from the provided URL.
    """
    try:
        logger.info(f"Starting scrape for URL: {url}")
        data = scrape_press_release(url)
        if data:
            store_in_db(data)
            return {"message": "Scraping and storage successful.", "data": data}
        else:
            raise HTTPException(status_code=404, detail="No data found at the provided URL.")
    except Exception as e:
        logger.error(f"Error scraping single release: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/scrape_all", tags=["Scrape"])
def scrape_all_endpoint(
    start_date: str = Query(..., description="Start date in YYYY-MM-DD format"),
    end_date: str = Query(..., description="End date in YYYY-MM-DD format"),
    ministry_id: str = Query('0', description="Ministry ID as per PIB website")
):
    """
    Scrapes all press releases between the provided start and end dates.
    """
    try:
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')
        if start_dt > end_dt:
            raise HTTPException(status_code=400, detail="Start date must be before end date.")

        logger.info(f"Starting scrape from {start_date} to {end_date} for ministry ID {ministry_id}")
        data = scrape_all_releases(start_dt, end_dt, ministry_id)
        if data:
            store_in_db(data)
            return {"message": "Scraping and storage successful.", "total_releases": len(data)}
        else:
            raise HTTPException(status_code=404, detail="No press releases found for the given date range.")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
    except Exception as e:
        logger.error(f"Error scraping all releases: {e}")
        raise HTTPException(status_code=500, detail=str(e))