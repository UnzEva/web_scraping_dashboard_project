import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go

# Connect to database
def get_data():
    conn = sqlite3.connect('baseball_cleaned.db')
    
    # Load all league data
    al_era = pd.read_sql("SELECT * FROM yearly_era_american_league", conn)
    nl_era = pd.read_sql("SELECT * FROM yearly_era_national_league", conn)
    al_strikeouts = pd.read_sql("SELECT * FROM yearly_strikeouts_american_league", conn)
    nl_strikeouts = pd.read_sql("SELECT * FROM yearly_strikeouts_national_league", conn)
    al_wins = pd.read_sql("SELECT * FROM yearly_wins_american_league", conn)
    nl_wins = pd.read_sql("SELECT * FROM yearly_wins_national_league", conn)
    
    conn.close()
    
    return al_era, nl_era, al_strikeouts, nl_strikeouts, al_wins, nl_wins

def create_team_performance_chart(data):
    """Create team performance scatter plot"""
    team_stats = data.groupby('Team').agg({
        'Strikeouts': 'mean',
        'Wins': 'mean',
        'ERA': 'mean'
    }).reset_index()
    
    fig = px.scatter(team_stats, x='Strikeouts', y='Wins', size='ERA',
                     color='ERA', hover_name='Team',
                     title='Team Performance: Strikeouts vs Wins (Bubble size = ERA)',
                     labels={'Strikeouts': 'Average Strikeouts', 'Wins': 'Average Wins'})
    fig.update_layout(height=500)
    return fig

def main():
    st.set_page_config(page_title="Baseball Stats", layout="wide")
    st.title("⚾ Baseball Pitching Statistics")
    
    # Load data
    al_era, nl_era, al_strikeouts, nl_strikeouts, al_wins, nl_wins = get_data()
    
    # Sidebar
    st.sidebar.header("Filters")
    
    # League selection
    selected_leagues = st.sidebar.multiselect(
        "Select Leagues",
        ["American League", "National League"],
        default=["American League", "National League"]
    )
    
    # Year selection - only use the years that are available in both leagues.
    common_years = sorted(set(al_era['Year']).intersection(set(nl_era['Year'])))
    selected_year = st.sidebar.selectbox("Select Year for Player Leaders", common_years[::-1])
    
    # Main tabs
    tab1, tab2, tab3 = st.tabs(["League Comparison", "Team Performance", "Player Leaders"])
    
    with tab1:
        st.header("League Comparison by Year")
        
        # prepare the data for league comparison, taking into account the filter
        def prepare_league_comparison(al_data, nl_data, stat_name):
            # only take the total years
            common_years_set = set(al_data['Year']).intersection(set(nl_data['Year']))
            
            comparison_data = []
            
            if "American League" in selected_leagues:
                al_avg = al_data[al_data['Year'].isin(common_years_set)].groupby('Year')[stat_name].mean().reset_index()
                al_avg['League'] = 'American League'
                comparison_data.append(al_avg)
            
            if "National League" in selected_leagues:
                nl_avg = nl_data[nl_data['Year'].isin(common_years_set)].groupby('Year')[stat_name].mean().reset_index()
                nl_avg['League'] = 'National League'
                comparison_data.append(nl_avg)
            
            if comparison_data:
                return pd.concat(comparison_data)
            else:
                return pd.DataFrame()
        
        # ERA comparison
        era_comparison = prepare_league_comparison(al_era, nl_era, 'ERA')
        if not era_comparison.empty:
            fig_era = px.line(era_comparison, x='Year', y='ERA', color='League',
                             title='Average ERA Comparison by Year (Lower is Better)')
            fig_era.update_layout(height=400)
            st.plotly_chart(fig_era, use_container_width=True)
        else:
            st.warning("Please select at least one league to display ERA comparison")
        
        # Strikeouts comparison
        strikeouts_comparison = prepare_league_comparison(al_strikeouts, nl_strikeouts, 'Strikeouts')
        if not strikeouts_comparison.empty:
            fig_strikeouts = px.line(strikeouts_comparison, x='Year', y='Strikeouts', color='League',
                                   title='Average Strikeouts Comparison by Year')
            fig_strikeouts.update_layout(height=400)
            st.plotly_chart(fig_strikeouts, use_container_width=True)
        else:
            st.warning("Please select at least one league to display Strikeouts comparison")
        
        # Wins comparison
        wins_comparison = prepare_league_comparison(al_wins, nl_wins, 'Wins')
        if not wins_comparison.empty:
            fig_wins = px.line(wins_comparison, x='Year', y='Wins', color='League',
                              title='Average Wins Comparison by Year')
            fig_wins.update_layout(height=400)
            st.plotly_chart(fig_wins, use_container_width=True)
        else:
            st.warning("Please select at least one league to display Wins comparison")
    
    with tab2:
        st.header("Team Performance Analysis")
        
        # Creating a combined dataframe for the scatter plot, taking into account the league filter
        combined_data_list = []
        
        if "American League" in selected_leagues:
            al_combined = pd.merge(al_era, al_strikeouts, on=['Year', 'Player', 'Team'])
            al_combined = pd.merge(al_combined, al_wins, on=['Year', 'Player', 'Team'])
            al_combined['League'] = 'American League'
            combined_data_list.append(al_combined)
        
        if "National League" in selected_leagues:
            nl_combined = pd.merge(nl_era, nl_strikeouts, on=['Year', 'Player', 'Team'])
            nl_combined = pd.merge(nl_combined, nl_wins, on=['Year', 'Player', 'Team'])
            nl_combined['League'] = 'National League'
            combined_data_list.append(nl_combined)
        
        if combined_data_list:
            combined_data = pd.concat(combined_data_list)
            
            # Creating scatter plot
            fig_team = create_team_performance_chart(combined_data)
            st.plotly_chart(fig_team, use_container_width=True)
            
            # Additional statistics on teams
            col1, col2 = st.columns(2)
            
            with col1:
                if "American League" in selected_leagues:
                    st.subheader("American League Team Stats")
                    
                    # Aggregating data by commands for AL
                    al_team_stats = al_combined.groupby('Team').agg({
                        'ERA': 'mean',
                        'Strikeouts': 'mean', 
                        'Wins': 'mean'
                    }).round(2).reset_index()
                    
                    st.dataframe(al_team_stats, use_container_width=True)
                else:
                    st.info("American League not selected")
            
            with col2:
                if "National League" in selected_leagues:
                    st.subheader("National League Team Stats")
                    
                    # Aggregating data by commands for NL
                    nl_team_stats = nl_combined.groupby('Team').agg({
                        'ERA': 'mean',
                        'Strikeouts': 'mean',
                        'Wins': 'mean'
                    }).round(2).reset_index()
                    
                    st.dataframe(nl_team_stats, use_container_width=True)
                else:
                    st.info("National League not selected")
        else:
            st.warning("Please select at least one league to display team performance")
    
    with tab3:
        st.header(f"Player Leaders - {selected_year}")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("ERA Leaders")
            era_leaders_list = []
            
            if "American League" in selected_leagues:
                al_era_year = al_era[al_era['Year'] == selected_year].nsmallest(5, 'ERA')
                era_leaders_list.append(al_era_year[['Player', 'Team', 'ERA']].assign(League='AL'))
            
            if "National League" in selected_leagues:
                nl_era_year = nl_era[nl_era['Year'] == selected_year].nsmallest(5, 'ERA')
                era_leaders_list.append(nl_era_year[['Player', 'Team', 'ERA']].assign(League='NL'))
            
            if era_leaders_list:
                era_leaders = pd.concat(era_leaders_list).head(10)
                st.dataframe(era_leaders, use_container_width=True)
            else:
                st.info("Select leagues to see ERA leaders")
        
        with col2:
            st.subheader("Strikeout Leaders")
            strikeout_leaders_list = []
            
            if "American League" in selected_leagues:
                al_strikeouts_year = al_strikeouts[al_strikeouts['Year'] == selected_year].nlargest(5, 'Strikeouts')
                strikeout_leaders_list.append(al_strikeouts_year[['Player', 'Team', 'Strikeouts']].assign(League='AL'))
            
            if "National League" in selected_leagues:
                nl_strikeouts_year = nl_strikeouts[nl_strikeouts['Year'] == selected_year].nlargest(5, 'Strikeouts')
                strikeout_leaders_list.append(nl_strikeouts_year[['Player', 'Team', 'Strikeouts']].assign(League='NL'))
            
            if strikeout_leaders_list:
                strikeout_leaders = pd.concat(strikeout_leaders_list).head(10)
                st.dataframe(strikeout_leaders, use_container_width=True)
            else:
                st.info("Select leagues to see Strikeout leaders")
        
        with col3:
            st.subheader("Win Leaders")
            win_leaders_list = []
            
            if "American League" in selected_leagues:
                al_wins_year = al_wins[al_wins['Year'] == selected_year].nlargest(5, 'Wins')
                win_leaders_list.append(al_wins_year[['Player', 'Team', 'Wins']].assign(League='AL'))
            
            if "National League" in selected_leagues:
                nl_wins_year = nl_wins[nl_wins['Year'] == selected_year].nlargest(5, 'Wins')
                win_leaders_list.append(nl_wins_year[['Player', 'Team', 'Wins']].assign(League='NL'))
            
            if win_leaders_list:
                win_leaders = pd.concat(win_leaders_list).head(10)
                st.dataframe(win_leaders, use_container_width=True)
            else:
                st.info("Select leagues to see Win leaders")
    
    # Footer with data info
    st.markdown("---")
    st.markdown(f"""
    **Data Information:**
    - American League data: {al_era['Year'].min()} - {al_era['Year'].max()}
    - National League data: {nl_era['Year'].min()} - {nl_era['Year'].max()}
    - Common years for comparison: {common_years[0]} - {common_years[-1]}
    """)

if __name__ == "__main__":
    main()