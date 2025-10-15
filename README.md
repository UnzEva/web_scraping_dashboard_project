# ⚾ Baseball Pitching Statistics Dashboard

A comprehensive web scraping and data visualization project for MLB (Major League Baseball) pitching statistics.

## Data Sources
The Official Baseball History Site: [Baseball Almanac](https://www.baseball-almanac.com/pimenu.shtml)

## Project Structure

1. **mlb_scraper.py** - Scrapes data from Baseball Almanac
2. **data_cleaner.py** - Cleans and processes raw data
3. **database_import.py** - Imports data to SQLite database
4. **query_program.py** - Command-line query interface
5. **dashboard.py** - Streamlit interactive dashboard

##
web_scraping_dashboard_project/

├── dashboard.py          
├── mlb_scraper.py       
├── data_cleaner.py       
├── database_import.py    
├── query_program.py     
├── requirements.txt     
├── baseball_cleaned.db    
└── README.md

## Installation

```bash 
git clone https://github.com/[yourusername]/web_scraping_dashboard_project.git
cd web_scraping_dashboard_project
pip install -r requirements.txt
```

## Usage

1. **Run the scraper:** `python mlb_scraper.py`
2. **Clean the data:** `python data_cleaner.py`
4. **Import to database:** `python database_import.py`
5. **Run queries:** `python query_program.py`
6. **Launch dashboard:** `streamlit run dashboard.py`

## Live Dashboard
The dashboard is deployed at: [Streamlit Dashboard](https://webscrapingdashboardproject.streamlit.app/)

This project is open source and free to use.
