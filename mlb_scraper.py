from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import os

def setup_driver():
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    return webdriver.Chrome(options=options)

def scrape_pitching_leaders():
    driver = setup_driver()
    
    # Only 3 main statistics - strikeouts, wins, ERA
    pages = [
        {
            'name': 'yearly_strikeouts',
            'url': 'https://www.baseball-almanac.com/pitching/pistrik4.shtml',
            'headers': ['Year_AL', 'AL_Player', 'AL_Strikeouts', 'AL_Team', 'Year_NL', 'NL_Player', 'NL_Strikeouts', 'NL_Team']
        },
        {
            'name': 'yearly_wins', 
            'url': 'https://www.baseball-almanac.com/pitching/piwins4.shtml',
            'headers': ['Year_AL', 'AL_Player', 'AL_Wins', 'AL_Team', 'Year_NL', 'NL_Player', 'NL_Wins', 'NL_Team']
        },
        {
            'name': 'yearly_era',
            'url': 'https://www.baseball-almanac.com/pitching/piera4.shtml',
            'headers': ['Year_AL', 'AL_Player', 'AL_ERA', 'AL_Team', 'Year_NL', 'NL_Player', 'NL_ERA', 'NL_Team']
        }
    ]
    
    all_data = {}
    
    for page in pages:
        try:
            print(f"Scraping {page['name']}...")
            driver.get(page['url'])
            time.sleep(3)
            
            table = driver.find_element(By.TAG_NAME, "table")
            rows = table.find_elements(By.TAG_NAME, "tr")
            
            data_rows = []
            for row in rows[1:]:
                cells = row.find_elements(By.TAG_NAME, "td")
                if cells and len(cells) == 8:
                    row_data = [cell.text.strip() for cell in cells]
                    data_rows.append(row_data)
            
            df = pd.DataFrame(data_rows, columns=page['headers'])
            all_data[page['name']] = df
            
            print(f"Saved {len(data_rows)} rows")
            
        except Exception as e:
            print(f"Error: {e}")
            continue
    
    driver.quit()
    return all_data

def main():
    os.makedirs('data', exist_ok=True)
    
    print("SCRAPING PITCHING LEADERS DATA")
    print("=" * 40)
    
    data = scrape_pitching_leaders()
    
    # Save individual files
    for name, df in data.items():
        filename = f"data/{name}.csv"
        df.to_csv(filename, index=False)
        print(f"Created: {filename}")
    
    # Create combined file
    if len(data) == 3:
        strikeouts = data['yearly_strikeouts']
        wins = data['yearly_wins']
        era = data['yearly_era']
        
        # Simple combined view
        combined = strikeouts[['Year_AL', 'AL_Player', 'AL_Team']].copy()
        combined['Strikeouts'] = strikeouts['AL_Strikeouts']
        combined['Wins'] = wins['AL_Wins']
        combined['ERA'] = era['AL_ERA']
        
        combined.to_csv('combined_pitching.csv', index=False)
        print("Created: combined_pitching.csv")
    
    print(f"\nTotal files created: {len(os.listdir('.'))}")

if __name__ == "__main__":
    main()