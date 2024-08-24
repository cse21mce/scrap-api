# PIB Press Releases Scraping API

## Overview

The PIB Press Releases Scraper is a FastAPI-based application designed to scrape and store press releases from the Press Information Bureau (PIB) of India. It provides endpoints to scrape single or multiple press releases based on specific criteria.

## Features

- Scrape detailed information from a single press release URL.
- Scrape all press releases within a specified date range.
- Store the scraped data in a database.

## Technologies Used

- **FastAPI**: Web framework for building APIs with Python 3.6+ based on standard Python type hints.
- **Uvicorn**: ASGI server for running the FastAPI application.
- **Requests**: HTTP library for making requests to external web pages.
- **BeautifulSoup**: HTML parser for extracting data from web pages.
- **Pymongo**: MongoDB driver for Python.

## Setup and Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/pib-press-releases-scraper.git
   cd pib-press-releases-scraper
   ```

2. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

### Environment Variables

Ensure you have the following environment variables set up for database configuration and other settings:

- MONGO_URI: The URI for your MongoDB instance.

You can use a .env file to manage these variables:

    MONGO_URI=mongodb://localhost:27017/mydatabase

### Requirements File

The requirements.txt file includes the following dependencies:

    fastapi==0.112.1
    uvicorn==0.30.6
    requests==2.32.3
    beautifulsoup4==4.12.3
    pymongo==4.8.0

### Usage

Running the Application

To start the FastAPI application locally, run:

    uvicorn app:app --host 0.0.0.0 --port 8000 --reload

### API Endpoints

**GET /: Returns a welcome message.**

    GET / HTTP/1.1

**GET /scrape_single: Scrapes a single press release from a provided URL.**

- Parameters:

  - url: The URL of the press release.

    ```bash
    GET /scrape_single?url=https://pib.gov.in/PressReleasePage.aspx?PRID=2048453
    ```

* Response:

  ```json
  response:
      {
      "title": "PM to visit Maharashtra and Rajasthan on 25th August",
      "date_posted": "Posted On: 24 AUG 2024 2:54PM by PIB Delhi",
      "ministry": "Prime Minister's Office",
      "content": "Prime Minister Shri Narendra Modi will visit Jalgaon in Maharashtra and Jodhpur in Rajasthan on 25th August. At around 11:15 AM, Prime Minister will participate in the Lakhpati Didi Sammelan. At around 4:30 PM, Prime Minister will be the Chief Guest at the concluding ceremony of Platinum Jubilee celebrations of the Rajasthan High Court in Jodhpur. PM in Maharashtra Prime Minister will visit Jalgaon to participate in Lakhpati Didi Sammelan. He will give certificates and felicitate 11 lakh new Lakhpati Didis, who recently became Lakhpati during the third term of NDA Government. Prime Minister will also interact with Lakhpati Didis from across the country. Prime Minister will release a Revolving Fund of Rs 2,500 crore which will benefit about 48 lakh members of 4.3 lakh Self-Help Groups (SHG). He will also disburse bank loan of Rs 5,000 crore which will benefit 25.8 lakh members of 2.35 lakh SHGs Since the inception of Lakhpati Didi Yoajna, one crore women have already been made Lakhpati Didis. The government has set a target to make 3 crore Lakhpati Didis. PM in Rajasthan Prime Minister will be the Chief Guest at the concluding ceremony of the Platinum Jubilee celebrations of the Rajasthan High Court, to be held at the High Court Campus, Jodhpur. Prime Minister will also inaugurate the Rajasthan High Court Museum. *** MJPS",
      "images": null,
      "url": "https://pib.gov.in/PressReleasePage.aspx?PRID=2048453"
      }

  ```

**GET /scrape_all: Scrapes all press releases within a specified date range.**

- Parameters:

  - start_date: Start date in YYYY-MM-DD format.

  - end_date: End date in YYYY-MM-DD format.

  - ministry_id: (Optional) Ministry ID as per PIB website.

    ```bash
    GET /scrape_all?start_date=2024-08-23&end_date=2024-08-24&ministry_id=0
    ```

- Response:

  ```json
  response: [
      {
          "url": "https://pib.gov.in/PressReleasePage.aspx?PRID=2048409",
          "content": "The Minister of Communications and Development of North Eastern Region Shri Jyotiraditya Scindia along with Dr Chandra Sekhar Pemmasani, Minister of State for Communications held the second meeting with the recently constituted Stakeholders Advisory Committee (SAC) on Telecom Service Providers (TSPs) on Friday. The initiative by the Department of Telecommunications (DoT) is aimed at engaging all stakeholders in expanding and shaping the future of India's telecommunication ecosystem and fostering inclusive and collaborative policy decision-making. During the first SAC on TSP, certain focus areas were identified. In today’s meeting, discussions centered about international standards and India’s share in Intellectual Property and Standard Essential Patent (SEP), connectivity gaps in telecom and quality of telecom services. SAC members emphasised systematically aligning research to ‘India’s needs’ and put in place a vibrant standards community. India has already taken various initiatives like launch of Bhart6G Vision and Bhart6G Alliance, patent and IPR support framework, commissioning of testbeds, etc., and country can aspire for achieving 10% of all 6G patents and 1/6th contributions to global standards promoting India’s needs. SAC proposed a 3-year roadmap for achieving it. The SAC expressed the view that, for India to become a deep tech leader, penetration of both wireline and intelligent wireless broadband networks, with reliable connectivity, is critical. The TSPs sought supportive policy framework to encourage investments towards the path of 100% broadband coverage in country. Various reasons and possible measures to improve the quality of telecom service were also discussed. Minister Shri Scindia asked the SAC members to define a critical path to achieve the targets discussed and to define roles they see for different stakeholders, including the government, in achieving the same. He also exhorted TSPs to take all necessary measure to ensure that citizens get good quality of telecom services. Had a productive meeting with the Advisory Group of Telecom Service providers. Discussed issues pertaining to quality of services, India’s 6G vision and promoting research and development to take our sector to new heights of development. pic.twitter.com/toSZOIxoUF Six distinct Stakeholders Advisory Committees (SACs) have been constituted by Minister Scindia to provide valuable insights to the DoT on various matters pertaining to it. They are aimed at facilitating a consistent two-way dialogue with government on matters related to telecommunication sector. Industry thought leaders, top CEOs, academicians, researchers, entrepreneurs and start-ups are members of six advisory committees (SACs). ******** AD/DK",
          "date_posted": "Posted On: 24 AUG 2024 9:48AM by PIB Delhi",
          "images": [
              "https://static.pib.gov.in/WriteReadData/userfiles/image/image001MB7B.jpg",
              "https://static.pib.gov.in/WriteReadData/userfiles/image/image0027SBQ.jpg",
              "https://static.pib.gov.in/WriteReadData/userfiles/image/image003ISG8.jpg",
              "https://static.pib.gov.in/WriteReadData/userfiles/image/image004OT5H.jpg",
              "https://static.pib.gov.in/WriteReadData/userfiles/image/image005I3WV.png"
              ],
          "ministry": "Ministry of Communications",
          "title": "Union Minister Shri Jyotiraditya Scindia holds second meeting of SAC on Telecom Service Providers"

      },
      {
          "url": "https://pib.gov.in/PressReleasePage.aspx?PRID=2048402",
          "content": "Raksha Mantri Shri Rajnath Singh met the US National Security Advisor Mr Jake Sullivan at the White House in Washington DC on August 23, 2024. They deliberated on the evolving geopolitical situation and certain key regional security issues. They also discussed the ongoing defence industrial collaboration projects between India and US, and potential areas where the industries of the two countries could work together. The Raksha Mantri also interacted with the senior leaders of the US defence industry at a round-table organised by US India Strategic Partnership Forum in Washington DC. The round-table was attended by a large number of US defence and technology companies. Shri Rajnath Singh emphasised that India welcomes US investment and technology collaboration, and is ready with a skilled human resource base, robust pro-FDI and pro-business ecosystem, and large domestic market. India looks forward to closely working with US across the domains of defence for capability building and for an abiding technology & industrial partnership which can address emerging challenges, he added. Later, the Raksha Mantri briefly met a delegation from US India Business Council. ******* ABB/Savvy",
          "date_posted": "Posted On: 24 AUG 2024 8:59AM by PIB Delhi",
          "images": null,
          "ministry": "Ministry of Defence",
          "title": "Raksha Mantri Shri Rajnath Singh meets US National Security Advisor Mr Jake Sullivan in Washington DC"
      },
      {...},
      {...}
  ]
  ```
