import requests
from bs4 import BeautifulSoup
import re

# Initialize a session to maintain the connection across requests
session = requests.Session()

def txt_cleaner(txt):
    """
    Cleans up text by removing extra whitespace, new lines, and carriage returns.
    
    Args:
    - txt (str): The text to be cleaned.
    
    Returns:
    - str: The cleaned text.
    """
    cleaned_string = txt.strip()  # Remove leading and trailing whitespace
    cleaned_string = cleaned_string.replace('\r', ' ').replace('\n', ' ')  # Replace carriage returns and new lines with spaces
    cleaned_string = re.sub(' +', ' ', cleaned_string)  # Replace multiple spaces with a single space
    return cleaned_string

def scrap_data():
    """
    Scrapes the main page to collect all URLs for detailed articles based on form data.
    
    Returns:
    - list: A list of dictionaries containing information scraped from each URL.
    """
    url = 'https://pib.gov.in/allRel.aspx'

    # this data is not working. Need Selennium to intract with the page
    # Data to be sent with the POST request to filter releases
    data = {
        'ctl00$ContentPlaceHolder1$ddlMinistry': '1',  # Ministry dropdown value
        'ctl00$ContentPlaceHolder1$ddlday': '2',      # Day dropdown value
        'ctl00$ContentPlaceHolder1$ddlMonth': '7',     # Month dropdown value (July)
        'ctl00$ContentPlaceHolder1$ddlYear': '2024',   # Year dropdown value
    }

    # Use a session to maintain the connection
    response = session.post(url, data=data)  # Perform the POST request with the specified data
    soup = BeautifulSoup(response.content, 'html.parser')  # Parse the response content with BeautifulSoup

    # Extract all URLs from the page to scrape further
    all_urls_to_scrape = []
    for a in soup.select('.content-area ul li a'):
        href = a.get('href')
        if href:
            all_urls_to_scrape.append('https://pib.gov.in' + href)  # Construct the full URL

    results = []
    for url in all_urls_to_scrape:
        info = scrap_url(url)  # Scrape data from each URL
        results.append(info)  # Append the scraped information to results
    
    return results

def scrap_url(url):
    """
    Scrapes detailed information from a specific URL.
    
    Args:
    - url (str): The URL of the article to scrape.
    
    Returns:
    - dict: A dictionary containing the title, date, content, ministry, and images of the article.
    """
    response = session.get(url)  # Perform the GET request for the specific URL
    soup = BeautifulSoup(response.content, 'html.parser')  # Parse the response content with BeautifulSoup

    # Extract text from paragraphs within the main content section
    all_text = ' '.join([p.get_text() for p in soup.select('.innner-page-main-about-us-content-right-part p')]).strip()
    
    # Extract image and iframe sources
    img_src = [img.get('src') for img in soup.select('div.innner-page-main-about-us-content-right-part img')]
    iframe_src = [iframe.get('src') for iframe in soup.select('div.innner-page-main-about-us-content-right-part iframe')]
    all_image_src = img_src + iframe_src  # Combine image and iframe sources

    # If no images are found, set all_image_src to None
    if len(all_image_src) == 0:
        all_image_src = None

    # Extract and clean text data from various elements
    info = {
        'title': txt_cleaner(soup.select_one('div h2').get_text() if soup.select_one('div h2') else ''),
        'date_posted': txt_cleaner(soup.select_one('div.ReleaseDateSubHeaddateTime').get_text() if soup.select_one('div.ReleaseDateSubHeaddateTime') else ''),
        'content': txt_cleaner(all_text),
        'ministry': txt_cleaner(soup.select_one('div.MinistryNameSubhead').get_text() if soup.select_one('div.MinistryNameSubhead') else ''),
        'images': all_image_src
    }
    return info
