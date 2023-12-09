import json
import sqlite3

# Read data from JSON file
with open('league_data.json', 'r') as file:
    data = json.load(file)

# Create or connect to an SQLite database
conn = sqlite3.connect('top_players.db')
cursor = conn.cursor()

# Create a table
cursor.execute('''CREATE TABLE IF NOT EXISTS Players
                  (Name TEXT, Rank INT, LP INT)''')

# Insert data into the table
for player in data['players']:
    cursor.execute("INSERT INTO Players (Name, Rank, LP) VALUES (?, ?, ?)",
                   (player['name'], player['rank'], player['lp']))

# Commit changes and close connection
conn.commit()
conn.close()

print("Data inserted into SQLite database.")