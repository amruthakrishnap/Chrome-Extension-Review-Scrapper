# Chrome Extension Reviews Scraper

This project is designed to scrape reviews and information about Chrome extensions from the Chrome Web Store and store the data in Supabase. It utilizes Playwright for browsing and scraping the web pages, BeautifulSoup for parsing the HTML content, and psycopg2 for database operations with Supabase.

## Prerequisites

- Python 3.7+
- Pip (Python package installer)
- Supabase Credentials
- To Set CRON Job : Need to Create Apify Account [Optional]

## Installation

1. **Clone the repository** (or download the script).

    ```bash
    git clone https://github.com/amruthakrishnap/Chrome-Extension-Reviews-Scraper.git
    cd Chrome-Extension-Reviews-Scraper
    ```

2. **Create and activate a virtual environment** (optional but recommended).

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required dependencies**.

    ```bash
    pip install -r requirements.txt
    playwright install
    ```


## Setup Supabase 

1. **Create Account on Supabase**

2. **Once You Create Supabase Account Go to SQL Editor and Then Paste This SQL code to Create Tables**
   
    ```bash
    CREATE TABLE extension_info (
    id SERIAL PRIMARY KEY,
    extension_name TEXT UNIQUE NOT NULL,
    extension_url TEXT,
    developer TEXT,
    overall_rating TEXT,
    total_rating TEXT,
    extension_type TEXT,
    total_users TEXT
    );
    
    CREATE TABLE extension_review (
        id SERIAL PRIMARY KEY,
        extension_name TEXT NOT NULL,
        name TEXT,
        date DATE,
        rating TEXT,
        review TEXT,
        helpful TEXT
    );

3. **Now Get your Supabase API URL and API Key From API Setting**
    Once you Get your ApiKey and URL replace those in main.py code or apify.py code.
## Usage

1. **Run the script**.

    ```bash
    python main.py
    ```

2. **Follow the prompt** 

    ```plaintext
    Enter Full Chrome Extention Review Link: 
    Example : "https://chromewebstore.google.com/detail/freezen-matevpn-chrome/acjlblgibpeochegbmidehmaphkhdoec/reviews"
    ```

3. **Congratulations Scraping Process Starts From Here**
   ```plaintext
    You will get each script running status..!
    Once the Scrapping get's over data will save to Supabase.
    ```



