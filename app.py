from fastapi import FastAPI, HTTPException, Query
from threading import Thread
from scrap import scrap_data, scrap_url
from db import store_in_db
from bson import ObjectId

app = FastAPI()

def convert_object_ids(data):
    if isinstance(data, dict):
        return {k: convert_object_ids(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_object_ids(item) for item in data]
    elif isinstance(data, ObjectId):
        return str(data)
    else:
        return data
    

@app.get("/")
def root():
    return {"message":"Welcome to Scrap API"}



@app.get("/scrap")
def scrape_endpoint(url: str = Query(None, description="The URL to scrape")):
    """
    Endpoint to scrape data either from a specified URL or the default set of URLs.

    Args:
    - url (str): Optional query parameter specifying a URL to scrape.

    Returns:
    - dict: The scraped data from the specified URL or from all default URLs.
    """
    scrape_results = []

    def run_scraping():
        """
        Function to perform the scraping task. It will call `scrape_url` if a URL is provided,
        otherwise it will call `scrape_data` to scrape all URLs.
        """
        nonlocal scrape_results
        # Determine which scraping function to use based on the presence of the URL parameter
        if url:
            scrape_results = scrap_url(url)
        else:
            scrape_results = scrap_data()

    # Attempt to run the scraping function in a separate thread
    try:
        # Create and start a thread to run the scraping function
        thread = Thread(target=run_scraping)
        thread.start()
        # Wait for the thread to finish execution
        thread.join()

        data = store_in_db(scrape_results,url)
        
        return convert_object_ids(data)
    
    except Exception as e:
        # Handle any exceptions that occur during scraping
        raise HTTPException(status_code=500, detail=str(e))

# Start the FastAPI application using Uvicorn server
if __name__ == "__main__":
    import uvicorn
    # Run the FastAPI application on the specified host and port with auto-reloading enabled
    # uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
    uvicorn.run(app)
