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
fig, axs = plt.subplots(2, 2, figsize=(15, 15))  # 2 rows, 2 columns

# First subplot
axs[0, 0].bar(['League of Legends', 'Dota2'], [lol_playtime, dota2_playtime], color=['DeepSkyBlue','green'])
axs[0, 0].set_xlabel('Game')
axs[0, 0].set_ylabel('Average Playtime (hours)')
axs[0, 0].set_title('Average Self-Reported Playtimes of League of Legends and Dota2')
axs[0, 0].set_yticks(range(0, 125, 5))

# Connect to SQLite database
conn = sqlite3.connect('dota2_db.sqlite')

# Execute the query and convert it into a pandas DataFrame
df_public_matches = pd.read_sql_query("SELECT * from publicMatches", conn)
df_pro_matches = pd.read_sql_query("SELECT * from proMatches", conn)

# Calculate the average duration for public and pro matches
df_public_matches['duration_seconds'] = pd.to_timedelta(df_public_matches['duration']).dt.total_seconds()
df_pro_matches['duration_seconds'] = pd.to_timedelta(df_pro_matches['duration']).dt.total_seconds()

# Calculate the averages
avg_duration_public_matches = df_public_matches['duration_seconds'].mean() / 60 # convert to minutes
avg_duration_pro_matches = df_pro_matches['duration_seconds'].mean() / 60 # convert to minutes

# Second subplot
names = ['Public Matches', 'Pro Matches']
values = [avg_duration_public_matches, avg_duration_pro_matches]

axs[0, 1].bar(names, values)
axs[0, 1].set_ylabel('Average Duration (minutes)')
axs[0, 1].set_title('Comparison of Average Durations for Public and Pro Matches')

# Load player data into DataFrame
df_pro_players = pd.read_sql_query("SELECT * from proPlayers", conn)

# Third subplot
axs[1, 0].hist(df_pro_players['kills'])
axs[1, 0].set_title('Histogram of Kills (proPlayers)')
axs[1, 0].set_xlabel('Kills')
axs[1, 0].set_ylabel('Frequency')

# Fourth subplot
axs[1, 1].hist(df_pro_players['deaths'])
axs[1, 1].set_title('Histogram of Deaths (proPlayers)')
axs[1, 1].set_xlabel('Deaths')
axs[1, 1].set_ylabel('Frequency')

# Automatically adjust subplot params for better spacing
plt.tight_layout()
plt.show()

conn.close()

time_slots = ['< 10', '10 - 20', '20 - 30', '30 - 40', '40+']
kda_values = [0.00, 3.67, 4.86, 3.76, 3.36]

# Create a line graph
plt.figure(figsize=(8, 5))  # Adjust the figure size if needed
plt.plot(time_slots, kda_values, marker='o', linestyle='-')

# Title and labels
plt.title('Average K/D/A vs Time Slot')
plt.xlabel('Time Slot')
plt.ylabel('Average K/D/A')

# Show grid
plt.grid(True)

# Rotate x-axis labels for better readability if needed
plt.xticks(rotation=45)

# Show the plot
plt.tight_layout()
plt.show()
