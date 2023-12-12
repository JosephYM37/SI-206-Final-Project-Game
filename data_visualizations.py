# Robin Jiao, Shawn Rao, Joseph Chen
# To visualize: average time spent between games, difference between pro level and normal engagement
import sqlite3
import requests
import matplotlib.pyplot as plt

conn = sqlite3.connect('games_database.db')
cursor = conn.cursor()

cursor.execute("SELECT Playtime FROM JoinedData WHERE Name = 'League of Legends'")
result = cursor.fetchone()
lol_playtime = result[0] if result else None

cursor.execute("SELECT Playtime FROM JoinedData WHERE Name = 'Dota 2'")
result = cursor.fetchone()
dota2_playtime = result[0] if result else None

plt.figure(figsize=(10, 10))
plt.bar(['League of Legends', 'Dota2'], [lol_playtime, dota2_playtime], color=['DeepSkyBlue','green'])
plt.xlabel('Game')
plt.ylabel('Average Playtime (hours)')
plt.title('Average Self-Reported Playtimes of League of Legends and Dota2')

plt.yticks(range(0, 125, 5))

plt.show()

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

plt.bar(names, values)
plt.ylabel('Average Duration (minutes)')
plt.title('Comparison of Average Durations for Public and Pro Matches')
plt.show()

    # Don't forget to close the connection when you're done
conn.close()
    #You may use a similar approach for displaying histograms for player data. 

    # Connect to SQLite database
conn = sqlite3.connect('dota2_db.sqlite')

    # Load player data into DataFrame
df_pro_players = pd.read_sql_query("SELECT * from proPlayers", conn)

   # Generating histograms
fig, axs = plt.subplots(2, 3, figsize=(15, 10)) 

axs[0, 0].hist(df_pro_players['kills'])
axs[0, 0].set_title('Histogram of Kills (proPlayers)')
axs[0, 0].set_xlabel('Kills')
axs[0, 0].set_ylabel('Frequency')

axs[0, 1].hist(df_pro_players['deaths'])
axs[0, 1].set_title('Histogram of Deaths (proPlayers)')
axs[0, 1].set_xlabel('Deaths')
axs[0, 1].set_ylabel('Frequency')

axs[0, 2].hist(df_pro_players['assists'])
axs[0, 2].set_title('Histogram of Assists (proPlayers)')
axs[0, 2].set_xlabel('Assists')
axs[0, 2].set_ylabel('Frequency')

axs[1, 0].hist(df_pro_players['rank_tier'])
axs[1, 0].set_title('Histogram of Rank Tiers (proPlayers)')
axs[1, 0].set_xlabel('Rank Tier')
axs[1, 0].set_ylabel('Frequency')

axs[1, 1].hist(df_pro_players['wins'])
axs[1, 1].set_title('Histogram of Wins (proPlayers)')
axs[1, 1].set_xlabel('Wins')
axs[1, 1].set_ylabel('Frequency')

axs[1, 2].hist(df_pro_players['losses'])
axs[1, 2].set_title('Histogram of Losses (proPlayers)')
axs[1, 2].set_xlabel('Losses')
axs[1, 2].set_ylabel('Frequency')

    # Automatically adjust subplot params for better spacing
plt.tight_layout()
plt.show()

conn.close()
