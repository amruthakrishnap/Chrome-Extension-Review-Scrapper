# Chrome Extension Reviews Scraper

This project is designed to scrape reviews and information about Chrome extensions from the Chrome Web Store and store the data in Supabase. It utilizes Playwright for browsing and scraping the web pages, BeautifulSoup for parsing the HTML content, and psycopg2 for database operations with Supabase.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Database Schema](#database-schema)
- [License](#license)

## Prerequisites
- Python 3.6 or higher
- Supabase account
- PostgreSQL database credentials from Supabase
- Google Chrome or Chromium

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/chrome-extension-reviews-scraper.git
   cd chrome-extension-reviews-scraper
2.Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
3.Install the required dependencies:
    ```sh
pip install -r requirements.txt


