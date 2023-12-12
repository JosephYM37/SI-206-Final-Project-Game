# Robin Jiao, Shawn Rao, Joseph Chen
# To visualize: average time spent between games, difference between pro level and normal engagement
import sqlite3
import requests
import matplotlib.pyplot as plt
import pandas as pd

# Connect to SQLite database
conn = sqlite3.connect('games_database.db')
cursor = conn.cursor()

cursor.execute("SELECT Playtime FROM JoinedData WHERE Name = 'League of Legends'")
result = cursor.fetchone()
lol_playtime = result[0] if result else None

cursor.execute("SELECT Playtime FROM JoinedData WHERE Name = 'Dota 2'")
result = cursor.fetchone()
dota2_playtime = result[0] if result else None

# Create a figure and a set of subplots
fig, axs = plt.subplots(1, 1, figsize=(10, 10))  # 1 row, 1 column

# First subplot
axs.bar(['League of Legends', 'Dota2'], [lol_playtime, dota2_playtime], color=['DeepSkyBlue','green'])
axs.set_xlabel('Game')
axs.set_ylabel('Average Playtime (hours)')
axs.set_title('Average Self-Reported Playtimes of League of Legends and Dota2')
axs.set_yticks(range(0, 125, 5))

plt.show()

 #data visualiztion
    # Connect to SQLite database
conn = sqlite3.connect('games_database.db')

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

time_slots = ['< 10', '10 - 20', '20 - 30', '30 - 40', '40+']
kda_values = [0.00, 3.67, 4.86, 3.76, 3.36]

# Create a line graph
plt.figure(figsize=(8, 5))  # Adjust the figure size if needed
plt.plot(time_slots, kda_values, marker='o', linestyle='-')

# Title and labels
plt.title('Average K/D/A vs Time Slot for League of Legends')
plt.xlabel('Time Slot')
plt.ylabel('Average K/D/A')

# Show grid
plt.grid(True)

# Rotate x-axis labels for better readability if needed
plt.xticks(rotation=45)

# Show the plot
plt.tight_layout()
plt.show()
