import requests
import json
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import time
# Import datetime to format duration
from datetime import timedelta

################################################
# Your name: Shawn Rao                         #
# Who you worked with: Robin Jiao, Joseph Chen #
# API Used: OpenDota API (22.0.0)              #
################################################

# Define the API endpoints with placeholders for parameters
api_endpoints = [
    'https://api.opendota.com/api/proPlayers',
    'https://api.opendota.com/api/players/{account_id}',
    'https://api.opendota.com/api/players/{account_id}/wl',
    'https://api.opendota.com/api/players/{account_id}/recentMatches',
    'https://api.opendota.com/api/proMatches',
    'https://api.opendota.com/api/publicMatches',
    'https://api.opendota.com/api/matches/{match_id}'
]

# A function to make requests to the API
def make_api_request(api_endpoint, params=None):
    try:
        
        print("API endpoint: ", api_endpoint)

        # GET request to the API endpoint
        response = requests.get(api_endpoint, params=params)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            return data
        else:
            print(f"Error: {response.status_code} - {response.text} for {api_endpoint}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
    
'''
def drop_tables():
    conn = sqlite3.connect('dota2_db.sqlite')
    cur = conn.cursor()

    cur.execute('DROP TABLE IF EXISTS proPlayers')
    cur.execute('DROP TABLE IF EXISTS proMatches')
    cur.execute('DROP TABLE IF EXISTS publicMatches')

    conn.commit()
    conn.close()
'''
#database section
def init_db():

    # Connect to SQLite database
    conn = sqlite3.connect('dota2_db.sqlite')

    # Cursor to execute SQLite commands
    cur = conn.cursor()

    # Create tables
    cur.execute('''
        CREATE TABLE IF NOT EXISTS proPlayers (
            playerId INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER,
            personaname TEXT,
            solo_competitive_rank INTEGER,
            competitive_rank INTEGER,
            rank_tier INTEGER,
            leaderboard_rank INTEGER,
            wins INTEGER,
            losses INTEGER,
            kills INTEGER,
            deaths INTEGER,
            assists INTEGER,
            kda REAL,
            match_id INTEGER,
            duration TEXT
        )
    ''')
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS proMatches (
            proMatchId INTEGER PRIMARY KEY AUTOINCREMENT,
            match_id INTEGER,
            duration TEXT
        )
    ''')
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS publicMatches (
            publicMatchId INTEGER PRIMARY KEY AUTOINCREMENT,
            match_id INTEGER,
            duration TEXT
        )
    ''')

    # Commit changes and close connection
    conn.commit()
    conn.close()

def main():

    #delete previous if they exist
    #drop_tables()

    # First, initialize the database and tables
    init_db()
    
    # Connect to SQLite database
    conn = sqlite3.connect('dota2_db.sqlite')
    cur = conn.cursor()

    # Get pro players' data
    pro_players_data = make_api_request(api_endpoints[0])
    
    if pro_players_data:
        print("Pro Players data:")
        # Iterate through each pro player and get additional information
        for player in pro_players_data[:25]:
            # Check if 'account_id' is present in the player's data
            if 'account_id' in player:
                account_id = player['account_id']

                # Get player info
                player_info = make_api_request(api_endpoints[1].format(account_id=account_id))
                time.sleep(1) # wait 1 second
                if player_info:
                    info = {
                        "account_id": account_id,
                        "personaname": player['personaname'],
                        "solo_competitive_rank": player_info['solo_competitive_rank'],
                        "competitive_rank": player_info['competitive_rank'],
                        "rank_tier": player_info['rank_tier'],
                        "leaderboard_rank": player_info['leaderboard_rank'],
                    }
                    print(json.dumps(info, indent=2))

                # Get win/loss data
                wl_data = make_api_request(api_endpoints[2].format(account_id=account_id))
                if wl_data:
                    wl_info = {
                        "wins": wl_data['win'],
                        "losses": wl_data['lose'],
                    }
                    print(json.dumps(wl_info, indent=2))
                    
                # Get recent matches data
                recent_matches_data = make_api_request(api_endpoints[3].format(account_id=account_id))
                if recent_matches_data:
                    for match in recent_matches_data:
                        duration_in_hours = str(timedelta(seconds=match['duration']))
                        match_info = {
                            "match_id": match['match_id'],
                            "duration": duration_in_hours,
                            "kills": match['kills'],
                            "deaths": match['deaths'],
                            "assists": match['assists']
                        }
                        print(json.dumps(match_info, indent=2))

                end = "=" * 50
                print(f"\n{end}\n")

                # Add a delay of 1 second between API requests 
                # to hopefully avoid the rate limiting issues
                time.sleep(1)

            # Insert each player info in the proPlayers table
            try:
                cur.execute('''INSERT OR REPLACE INTO proPlayers (playerId, account_id, personaname, solo_competitive_rank, competitive_rank, rank_tier, leaderboard_rank, 
                            wins, losses, kills, deaths, assists, match_id, duration)
                            VALUES ((SELECT playerId FROM proPlayers WHERE account_id = ?), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                            (info['account_id'], info['account_id'], info['personaname'],
                            info['solo_competitive_rank'], info['competitive_rank'], info['rank_tier'], info['leaderboard_rank'], wl_info['wins'], wl_info['losses'], 
                            match_info['kills'], match_info['deaths'], match_info['assists'], match_info['match_id'], match_info['duration'])
                )
            except sqlite3.IntegrityError:
                pass

            conn.commit()

            # Print player info        
            print(json.dumps(info, indent=2))

    # Get pro matches data
    pro_matches_data = make_api_request(api_endpoints[4])

    if pro_matches_data:
        for match in pro_matches_data[:25]:
            
            specific_pro_match_id = match.get('match_id')
            
            if specific_pro_match_id:
                time.sleep(1) # wait 1 second
                # Get details for a specific pro match using match ID from pro players' data
                specific_pro_match_data = make_api_request(api_endpoints[6].replace('{match_id}', str(specific_pro_match_id)))

                if specific_pro_match_data:
                    match_info = {
                        'match_id': specific_pro_match_id,
                        'duration': str(timedelta(seconds=specific_pro_match_data.get('duration')))
                    }
                    try:
                        cur.execute('''INSERT OR REPLACE INTO proMatches (proMatchId, match_id, duration)
                                        VALUES ((SELECT proMatchId FROM proMatches WHERE match_id = ?), ?, ?)''',
                                        (match_info['match_id'], match_info['match_id'], match_info['duration'])
                                    )
                    except sqlite3.IntegrityError:
                        pass
                    #print(",".join(str(v) for v in match_info.values()))
                conn.commit()

            # Print match info
            print(json.dumps(match_info, indent=2))
                


    # Get public matches data
    public_matches_data = make_api_request(api_endpoints[5])

    if public_matches_data:
        for match in public_matches_data[:25]:
            
            specific_public_match_id = match.get('match_id')
            
            if specific_public_match_id:
                time.sleep(1) # wait 1 second
                specific_public_match_data = make_api_request(api_endpoints[6].replace('{match_id}', str(specific_public_match_id)))
                
                if specific_public_match_data:
                    match_info = {
                        'match_id': specific_public_match_id,
                        'duration': str(timedelta(seconds=specific_public_match_data.get('duration')))
                    }
                    try:
                        cur.execute('''INSERT OR REPLACE INTO publicMatches (publicMatchId, match_id, duration)
                                        VALUES ((SELECT publicMatchId FROM publicMatches WHERE match_id = ?), ?, ?)''',
                                        (match_info['match_id'], match_info['match_id'], match_info['duration'])
                                    )
                    except sqlite3.IntegrityError:
                        pass
                conn.commit()

                # Print match info
                print(json.dumps(match_info, indent=2))

    # Close connection to database when done
    conn.close()

    #data visualiztion
    # Connect to SQLite database
    conn = sqlite3.connect('dota2_db.sqlite')

    # Execute the query and convert it into a pandas DataFrame
    df_public_matches = pd.read_sql_query("SELECT * from publicMatches", conn)
    df_pro_matches = pd.read_sql_query("SELECT * from proMatches", conn)

    # Calculate the average duration for public and pro matches
    # The duration column is currently a string in the format "HH:MM:SS". We need to convert it to seconds for calculation.
    df_public_matches['duration_seconds'] = pd.to_timedelta(df_public_matches['duration']).dt.total_seconds()
    df_pro_matches['duration_seconds'] = pd.to_timedelta(df_pro_matches['duration']).dt.total_seconds()

    # Calculate the averages
    avg_duration_public_matches = df_public_matches['duration_seconds'].mean() / 60 # convert to minutes
    avg_duration_pro_matches = df_pro_matches['duration_seconds'].mean() / 60 # convert to minutes

    # Plot the bar chart
    names = ['Public Matches', 'Pro Matches']
    values = [avg_duration_public_matches, avg_duration_pro_matches]

    # For bar chart
    plt.bar(names, values, color=['blue', 'red'])
    plt.ylabel('Average Duration (minutes)', fontsize=12, weight='bold')
    plt.title('Comparison of Average Durations for Public and Pro Matches from OpenDota API', fontsize=14, weight='bold')
    plt.show()

    # Don't forget to close the connection when you're done
    conn.close()
    #You may use a similar approach for displaying histograms for player data. 

    # Connect to SQLite database
    conn = sqlite3.connect('dota2_db.sqlite')

    # Load player data into DataFrame
    df_pro_players = pd.read_sql_query("SELECT * from proPlayers", conn)

   # For histograms
    plt.figure(figsize=(5,5))
    plt.hist(df_pro_players['kills'], color='blue', edgecolor='black', linewidth=1.2, bins=20)
    plt.title('Histogram of Kills (proPlayers) from OpenDota API', weight='bold')
    plt.xlabel('Kills', fontsize=14)
    plt.ylabel('Frequency', fontsize=14)
    plt.show()

    plt.figure(figsize=(5,5))
    plt.hist(df_pro_players['deaths'], color='red', edgecolor='black', linewidth=1.2, bins=20)
    plt.title('Histogram of Deaths (proPlayers) from OpenDota API', weight='bold')
    plt.xlabel('Deaths', fontsize=14)
    plt.ylabel('Frequency', fontsize=14)
    plt.show()

    plt.figure(figsize=(5,5))
    plt.hist(df_pro_players['assists'], color='green', edgecolor='black', linewidth=1.2, bins=20)
    plt.title('Histogram of Assists (proPlayers) from OpenDota API', weight='bold')
    plt.xlabel('Assists', fontsize=14)
    plt.ylabel('Frequency', fontsize=14)
    plt.show()

    plt.figure(figsize=(5,5))
    plt.hist(df_pro_players['rank_tier'], color='purple', edgecolor='black', linewidth=1.2, bins=20)
    plt.title('Histogram of Rank Tiers (proPlayers) from OpenDota API', weight='bold')
    plt.xlabel('Rank Tier', fontsize=14)
    plt.ylabel('Frequency', fontsize=14)
    plt.show()

    plt.figure(figsize=(5,5))
    plt.hist(df_pro_players['wins'], color='orange', edgecolor='black', linewidth=1.2, bins=20)
    plt.title('Histogram of Wins (proPlayers) from OpenDota API', weight='bold')
    plt.xlabel('Wins', fontsize=14)
    plt.ylabel('Frequency', fontsize=14)
    plt.show()

    plt.figure(figsize=(5,5))
    plt.hist(df_pro_players['losses'], color='pink', edgecolor='black', linewidth=1.2, bins=20)
    plt.title('Histogram of Losses (proPlayers) from OpenDota API', weight='bold')
    plt.xlabel('Losses', fontsize=14)
    plt.ylabel('Frequency', fontsize=14)
    plt.show()
  
    conn.close()

if __name__ == "__main__":
    main()