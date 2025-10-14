import sqlite3
import pandas as pd

def show_tables(conn):
    """Show all tables in database"""
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    print("\nAvailable tables:")
    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"- {table_name} ({count} rows)")

def run_query(conn, query):
    """Run SQL query and display results"""
    try:
        df = pd.read_sql_query(query, conn)
        if df.empty:
            print("No results found")
        else:
            print(f"\nResults ({len(df)} rows):")
            print(df.to_string(index=False))
    except Exception as e:
        print(f"Error: {e}")

def main():
    # Connect to database
    conn = sqlite3.connect('baseball_cleaned.db')
    
    print("Baseball Statistics Query Tool")
    print("=" * 40)
    
    while True:
        print("\nOptions:")
        print("1. Show tables")
        print("2. Run custom query")
        print("3. Run example queries")
        print("4. Exit")
        
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == '1':
            show_tables(conn)
        
        elif choice == '2':
            query = input("\nEnter SQL query: ").strip()
            if query:
                run_query(conn, query)
        
        elif choice == '3':
            print("\nExample queries:")
            print("1. Top 10 strikeout leaders")
            print("2. Compare AL and NL ERA leaders")
            print("3. Players with most wins")
            
            example_choice = input("\nSelect example (1-3): ").strip()
            
            if example_choice == '1':
                query = """
                SELECT Year, Player, Team, Strikeouts 
                FROM combined_pitching_clean 
                ORDER BY Strikeouts DESC 
                LIMIT 10
                """
            elif example_choice == '2':
                query = """
                SELECT 'AL' as League, Year, Player, ERA, Team
                FROM yearly_era_american_league
                WHERE Year = 2023
                UNION ALL
                SELECT 'NL' as League, Year, Player, ERA, Team  
                FROM yearly_era_national_league
                WHERE Year = 2023
                ORDER BY ERA ASC
                LIMIT 10
                """
            elif example_choice == '3':
                query = """
                SELECT Year, Player, Team, Wins
                FROM combined_pitching_clean
                ORDER BY Wins DESC
                LIMIT 10
                """
            else:
                print("Invalid choice")
                continue
            
            run_query(conn, query)
        
        elif choice == '4':
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice")
    
    conn.close()

if __name__ == "__main__":
    main()