import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
import logging
from urllib.parse import urljoin

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize a session to maintain the connection across requests
session = requests.Session()

BASE_URL = 'https://pib.gov.in/allRel.aspx'
PRESS_RELEASE_BASE_URL = 'https://pib.gov.in/PressReleasePage.aspx'

def txt_cleaner(txt):
    """
    Cleans up text by removing extra whitespace, new lines, and carriage returns.
    
    Args:
    - txt (str): The text to be cleaned.
    
    Returns:
    - str: The cleaned text.
    """
    if txt:
        cleaned_string = txt.strip()
        cleaned_string = re.sub(r'\s+', ' ', cleaned_string)
        return cleaned_string
    return ''

def get_form_data():
    """
    Fetches the necessary form data including __VIEWSTATE and __EVENTVALIDATION.
    
    Returns:
    - dict: A dictionary containing form data.
    """
    response = session.get(BASE_URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    form_data = {}
    for input_tag in soup.find_all('input', type='hidden'):
        name = input_tag.get('name')
        value = input_tag.get('value', '')
        if name:
            form_data[name] = value

    return form_data

def get_press_releases(date: datetime, ministry_id: str = '0'):
    """
    Fetches all press releases for a specific date and ministry.
    """
    try:
        # Prepare date components
        day = date.day
        month = date.month
        year = date.year

        # Prepare payload for POST request
        form_data = get_form_data()  # Get the form data needed for the POST request
        payload = {
            'MinistryID': ministry_id,
            'MonthID': str(month),
            'YearID': str(year),
            'DateID': str(day),
            # Include the form data fetched earlier
            **form_data
        }

        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        response = session.post(BASE_URL, data=payload, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all press release entries
        content_area = soup.find('div', class_='content-area')
        if not content_area:
            logger.info(f"No press releases found for {date.strftime('%Y-%m-%d')}")
            return []

        releases = []
        for ul in content_area.find_all('ul'):
            ministry_header = ul.find('h3', class_='font104')
            if ministry_header:
                ministry_name = ministry_header.text.strip()
                for li in ul.find_all('li'):
                    a_tag = li.find('a', href=True)
                    if a_tag:
                        title = a_tag.text.strip()
                        relative_url = a_tag['href']
                        full_url = urljoin(BASE_URL, relative_url)
                        releases.append({
                            'title': title,
                            'url': full_url,
                            'ministry': ministry_name,
                            'date': date.strftime('%Y-%m-%d')
                        })
        logger.info(f"Found {len(releases)} releases for {date.strftime('%Y-%m-%d')}")
        return releases

    except Exception as e:
        logger.error(f"Error fetching press releases for {date.strftime('%Y-%m-%d')}: {e}")
        return []

def scrape_all_releases(start_date: datetime, end_date: datetime, ministry_id: str = '0'):
    """
    Scrapes all press releases between start_date and end_date for a given ministry.
    """
    try:
        current_date = start_date
        all_releases = []
        seen_urls = set()  # Track URLs to avoid duplicates

        while current_date <= end_date:
            logger.info(f"Fetching releases for {current_date.strftime('%Y-%m-%d')}")
            daily_releases = get_press_releases(current_date, ministry_id)

            for release in daily_releases:
                if release['url'] not in seen_urls:
                    logger.info(f"Scraping release: {release['title']}")
                    detailed_release = scrape_press_release(release['url'])
                    if detailed_release:
                        all_releases.append(detailed_release)
                        seen_urls.add(release['url'])
                else:
                    logger.info(f"Skipping duplicate URL: {release['url']}")

            current_date += timedelta(days=1)

        logger.info(f"Scraped a total of {len(all_releases)} releases between {start_date.strftime('%Y-%m-%d')} and {end_date.strftime('%Y-%m-%d')}")
        return all_releases

    except Exception as e:
        logger.error(f"Error scraping releases between dates: {e}")
        return []

def scrape_press_release(url: str):
    """
    Scrapes detailed information from a single press release URL.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0',
        }
        response = session.get(url, headers=headers)
        response.raise_for_status()

        # Print out the HTML content for debugging
        html_content = response.text
        logger.debug(f"HTML Content: {html_content[:2000]}")  # Print the first 2000 characters

        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract text from paragraphs within the main content section
        all_text = ' '.join([p.get_text() for p in soup.select('.innner-page-main-about-us-content-right-part p')]).strip()
    

        # Extract title
        title = txt_cleaner(soup.select_one('div h2').get_text() if soup.select_one('div h2') else 'No Title')

        # Extract date posted
        date_posted = txt_cleaner(soup.select_one('div.ReleaseDateSubHeaddateTime').get_text() if soup.select_one('div.ReleaseDateSubHeaddateTime') else 'No Date Provided')

        # Extract ministry
        ministry =  txt_cleaner(soup.select_one('div.MinistryNameSubhead').get_text() if soup.select_one('div.MinistryNameSubhead') else 'No Ministry Provided')

        # Extract content
        content = txt_cleaner(all_text)

        # Extract images
        
        img_src = [img.get('src') for img in soup.select('div.innner-page-main-about-us-content-right-part img')]
        iframe_src = [iframe.get('src') for iframe in soup.select('div.innner-page-main-about-us-content-right-part iframe')]
        all_image_src = img_src + iframe_src  # Combine image and iframe sources
        if len(all_image_src) == 0:
            all_image_src = None

        data = {
            'title': title,
            'date_posted': date_posted,
            'ministry': ministry,
            'content': content,
            'images': all_image_src,
            'url': url
        }

        logger.info(f"Successfully scraped data from {url}")
        return data

    except Exception as e:
        logger.error(f"Error scraping press release from {url}: {e}")
        return None

