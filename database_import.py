import sqlite3
import pandas as pd
import os
import glob

def create_database_schema(conn):
    """Create database schema with cleaned table structures"""
    
    tables_schema = {
        'combined_pitching_clean': """
            CREATE TABLE IF NOT EXISTS combined_pitching_clean (
                Year INTEGER,
                Player TEXT,
                Team TEXT,
                Strikeouts INTEGER,
                Wins INTEGER,
                ERA REAL
            )
        """,
        'yearly_era_american_league': """
            CREATE TABLE IF NOT EXISTS yearly_era_american_league (
                Year INTEGER,
                Player TEXT,
                ERA REAL,
                Team TEXT
            )
        """,
        'yearly_era_national_league': """
            CREATE TABLE IF NOT EXISTS yearly_era_national_league (
                Year INTEGER,
                Player TEXT,
                ERA REAL,
                Team TEXT
            )
        """,
        'yearly_strikeouts_american_league': """
            CREATE TABLE IF NOT EXISTS yearly_strikeouts_american_league (
                Year INTEGER,
                Player TEXT,
                Strikeouts INTEGER,
                Team TEXT
            )
        """,
        'yearly_strikeouts_national_league': """
            CREATE TABLE IF NOT EXISTS yearly_strikeouts_national_league (
                Year INTEGER,
                Player TEXT,
                Strikeouts INTEGER,
                Team TEXT
            )
        """,
        'yearly_wins_american_league': """
            CREATE TABLE IF NOT EXISTS yearly_wins_american_league (
                Year INTEGER,
                Player TEXT,
                Wins INTEGER,
                Team TEXT
            )
        """,
        'yearly_wins_national_league': """
            CREATE TABLE IF NOT EXISTS yearly_wins_national_league (
                Year INTEGER,
                Player TEXT,
                Wins INTEGER,
                Team TEXT
            )
        """
    }
    
    cursor = conn.cursor()
    for table_name, schema in tables_schema.items():
        cursor.execute(schema)
        print(f"Created table: {table_name}")
    
    conn.commit()

def import_cleaned_data(conn):
    """Import all cleaned CSV files to database"""
    
    cleaned_files = glob.glob('cleaned_data/*.csv')
    
    for file_path in cleaned_files:
        try:
            table_name = os.path.basename(file_path).replace('.csv', '')
            print(f"Importing {table_name}...")
            
            df = pd.read_csv(file_path)
            df.to_sql(table_name, conn, if_exists='replace', index=False)
            
            # Verify import
            cursor = conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            
            print(f"Imported {count} rows")
            
        except Exception as e:
            print(f"Error importing {table_name}: {e}")

def show_database_summary(conn):
    """Show summary of database contents"""
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    print("\nDATABASE SUMMARY:")
    print("=" * 50)
    
    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        print(f"\n{table_name}:")
        print(f"  Rows: {count}")
        print(f"  Columns: {', '.join(column_names)}")

def query_interface(conn):
    """Interactive SQL query interface"""
    
    print("\nINTERACTIVE SQL QUERY INTERFACE")
    print("Type 'exit' to quit, 'tables' to list tables, 'help' for examples")
    print("=" * 60)
    
    while True:
        try:
            query = input("\nSQL> ").strip()
            
            if query.lower() == 'exit':
                break
            elif query.lower() == 'tables':
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = cursor.fetchall()
                print("Available tables:")
                for table in tables:
                    cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
                    count = cursor.fetchone()[0]
                    print(f"  - {table[0]} ({count} rows)")
                continue
            elif query.lower() == 'help':
                show_query_examples()
                continue
            elif not query:
                continue
            
            # Execute query
            df = pd.read_sql_query(query, conn)
            print(f"\nResults ({len(df)} rows):")
            if len(df) > 0:
                print(df.head(20))  # Show first 20 rows
            else:
                print("No results found.")
                
        except Exception as e:
            print(f"Query error: {e}")

def show_query_examples():
    """Show example SQL queries"""
    print("\nEXAMPLE QUERIES:")
    print("1. View combined pitching data for recent years:")
    print("   SELECT * FROM combined_pitching_clean WHERE Year >= 2020 LIMIT 10;")
    print("\n2. Top ERA leaders in American League:")
    print("   SELECT * FROM yearly_era_american_league ORDER BY ERA ASC LIMIT 10;")
    print("\n3. Join strikeouts and wins for American League:")
    print("   SELECT s.Year, s.Player, s.Strikeouts, w.Wins")
    print("   FROM yearly_strikeouts_american_league s")
    print("   JOIN yearly_wins_american_league w ON s.Player = w.Player AND s.Year = w.Year")
    print("   WHERE s.Year = 2023;")
    print("\n4. Compare leagues for a specific year:")
    print("   SELECT 'AL' as League, Player, Strikeouts FROM yearly_strikeouts_american_league WHERE Year = 2023")
    print("   UNION ALL")
    print("   SELECT 'NL' as League, Player, Strikeouts FROM yearly_strikeouts_national_league WHERE Year = 2023")
    print("   ORDER BY Strikeouts DESC LIMIT 10;")

def main():
    """Main function"""
    print("BASEBALL STATISTICS DATABASE IMPORT")
    print("=" * 50)
    
    # Check if cleaned data exists in current directory
    if not os.path.exists('cleaned_data'):
        print("Error: 'cleaned_data' folder not found. Run data_cleaner.py first.")
        return
    
    # Create database connection
    conn = sqlite3.connect('baseball_cleaned.db')
    
    try:
        # Create schema and import data
        create_database_schema(conn)
        import_cleaned_data(conn)
        show_database_summary(conn)
        
        # Start query interface
        query_interface(conn)
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
        print("\nDatabase connection closed.")

if __name__ == "__main__":
    main()