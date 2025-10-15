# ⚾ Baseball Pitching Statistics Dashboard

A comprehensive web scraping and data visualization project for MLB (Major League Baseball) pitching statistics.

## Data Sources
Baseball Almanac

## Project Structure

1. **mlb_scraper.py** - Scrapes data from Baseball Almanac
2. **data_cleaner.py** - Cleans and processes raw data
3. **database_import.py** - Imports data to SQLite database
4. **query_program.py** - Command-line query interface
5. **dashboard.py** - Streamlit interactive dashboard

web_scraping_dashboard_project/

├── dashboard.py          
├── mlb_scraper.py       
├── data_cleaner.py       
├── database_import.py    
├── query_program.py     
├── requirements.txt     
├── baseball_stats.db    
└── README.md

## Installation

```bash 
git clone https://github.com/yourusername/web_scraping_dashboard_project.git
cd web_scraping_dashboard_project
pip install -r requirements.txt
```

## Usage

1. **Run the scraper:** `python src/mlb_scraper.py`
2. **Clean the data:** `python src/data_cleaner.py`
3. **Import to database:** `python src/database_import.py`
4. **Run queries:** `python src/query_program.py`
5. **Launch dashboard:** `streamlit run src/dashboard.py`

## Live Dashboard
The dashboard is deployed at: [[Streamlit Dashboard](https://webscrapingdashboardproject.streamlit.app/)]
