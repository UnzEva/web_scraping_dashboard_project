import pandas as pd
import os
import glob

def clean_combined_pitching():
    """Clean combined_pitching.csv"""
    print("Cleaning combined_pitching.csv...")
    
    df = pd.read_csv('data/combined_pitching.csv')
    
    # Remove first and last row (header duplicates)
    df = df.iloc[1:-1]
    
    # Remove rows with '-' in Year_AL (empty years 1876-1900)
    df = df[df['Year_AL'] != '-']
    
    # Convert Year to integer
    df['Year_AL'] = pd.to_numeric(df['Year_AL'], errors='coerce').astype('Int64')
    
    # Clean numeric columns
    df['Strikeouts'] = pd.to_numeric(df['Strikeouts'], errors='coerce')
    df['Wins'] = pd.to_numeric(df['Wins'], errors='coerce')
    df['ERA'] = pd.to_numeric(df['ERA'], errors='coerce')
    
    # Rename columns to consistent format
    df = df.rename(columns={
        'Year_AL': 'Year',
        'AL_Player': 'Player',
        'AL_Team': 'Team'
    })
    
    # Remove rows where all stats are null
    df = df.dropna(subset=['Strikeouts', 'Wins', 'ERA'], how='all')
    
    return df

def split_and_clean_yearly_data(filename, stat_name):
    """Split yearly data into American and National League tables"""
    print(f"Cleaning and splitting {filename}...")
    
    df = pd.read_csv(f'data/{filename}')
    
    # Remove first and last row (header duplicates)
    df = df.iloc[1:-1]
    
    # Create American League table
    al_df = df.iloc[:, :4].copy()
    al_df.columns = ['Year', 'Player', stat_name, 'Team']
    
    # Create National League table  
    nl_df = df.iloc[:, 4:].copy()
    nl_df.columns = ['Year', 'Player', stat_name, 'Team']
    
    # Remove rows with '-' in Year (empty years 1876-1900)
    al_df = al_df[al_df['Year'] != '-']
    nl_df = nl_df[nl_df['Year'] != '-']
    
    # Convert Year to integer
    al_df['Year'] = pd.to_numeric(al_df['Year'], errors='coerce').astype('Int64')
    nl_df['Year'] = pd.to_numeric(nl_df['Year'], errors='coerce').astype('Int64')
    
    # Clean numeric column based on stat type
    if stat_name == 'ERA':
        al_df[stat_name] = pd.to_numeric(al_df[stat_name], errors='coerce')
        nl_df[stat_name] = pd.to_numeric(nl_df[stat_name], errors='coerce')
    else:
        al_df[stat_name] = pd.to_numeric(al_df[stat_name], errors='coerce')
        nl_df[stat_name] = pd.to_numeric(nl_df[stat_name], errors='coerce')
    
    # Remove rows where stat is null
    al_df = al_df.dropna(subset=[stat_name])
    nl_df = nl_df.dropna(subset=[stat_name])
    
    return al_df, nl_df

def clean_all_data():
    """Clean all CSV files in data folder"""
    
    # Create cleaned_data directory in current folder (src)
    os.makedirs('cleaned_data', exist_ok=True)
    
    print("DATA CLEANING PROCESS")
    print("=" * 50)
    
    # Clean combined_pitching
    combined_clean = clean_combined_pitching()
    combined_clean.to_csv('cleaned_data/combined_pitching_clean.csv', index=False)
    print(f"Saved combined_pitching_clean.csv with {len(combined_clean)} rows")
    
    # Clean and split yearly_era
    era_al, era_nl = split_and_clean_yearly_data('yearly_era.csv', 'ERA')
    era_al.to_csv('cleaned_data/yearly_era_american_league.csv', index=False)
    era_nl.to_csv('cleaned_data/yearly_era_national_league.csv', index=False)
    print(f"Saved yearly_era_american_league.csv with {len(era_al)} rows")
    print(f"Saved yearly_era_national_league.csv with {len(era_nl)} rows")
    
    # Clean and split yearly_strikeouts
    so_al, so_nl = split_and_clean_yearly_data('yearly_strikeouts.csv', 'Strikeouts')
    so_al.to_csv('cleaned_data/yearly_strikeouts_american_league.csv', index=False)
    so_nl.to_csv('cleaned_data/yearly_strikeouts_national_league.csv', index=False)
    print(f"Saved yearly_strikeouts_american_league.csv with {len(so_al)} rows")
    print(f"Saved yearly_strikeouts_national_league.csv with {len(so_nl)} rows")
    
    # Clean and split yearly_wins
    wins_al, wins_nl = split_and_clean_yearly_data('yearly_wins.csv', 'Wins')
    wins_al.to_csv('cleaned_data/yearly_wins_american_league.csv', index=False)
    wins_nl.to_csv('cleaned_data/yearly_wins_national_league.csv', index=False)
    print(f"Saved yearly_wins_american_league.csv with {len(wins_al)} rows")
    print(f"Saved yearly_wins_national_league.csv with {len(wins_nl)} rows")
    
    # Summary
    print("\nCLEANING SUMMARY:")
    print("-" * 30)
    cleaned_files = glob.glob('cleaned_data/*.csv')
    for file in cleaned_files:
        df = pd.read_csv(file)
        print(f"{os.path.basename(file)}: {len(df)} rows")
    
    return True

def verify_data_quality():
    """Verify that data cleaning was successful"""
    print("\nDATA QUALITY CHECK:")
    print("=" * 30)
    
    cleaned_files = glob.glob('cleaned_data/*.csv')
    
    for file in cleaned_files:
        df = pd.read_csv(file)
        filename = os.path.basename(file)
        
        print(f"\n{filename}:")
        print(f"  Total rows: {len(df)}")
        print(f"  Columns: {list(df.columns)}")
        
        # Check data types
        for col in df.columns:
            if col == 'Year':
                print(f"  {col}: {df[col].dtype}, range: {df[col].min()}-{df[col].max()}")
            elif col in ['Strikeouts', 'Wins']:
                print(f"  {col}: {df[col].dtype}, max: {df[col].max()}")
            elif col == 'ERA':
                print(f"  {col}: {df[col].dtype}, min: {df[col].min()}")
        
        # Check for null values
        null_counts = df.isnull().sum()
        if null_counts.sum() > 0:
            print(f"  Null values: {dict(null_counts[null_counts > 0])}")

if __name__ == "__main__":
    # Check if data directory exists
    if not os.path.exists('data'):
        print("Error: 'data' folder not found. Run mlb_scraper.py first.")
    else:
        if clean_all_data():
            verify_data_quality()