import unittest
import sqlite3
import json
import os
import matplotlib.pyplot as plt
import requests

api_key = "34cf19bf45874c2c9d0ed8defa498b17"
api_url = f"https://api.rawg.io/api/games"
api_url = api_url + '?key=' + api_key

# Define the tag and ordering
tag = 'MOBA'
ordering = '-rating'

# Make the API request
response = requests.get(f'{api_url}&tags={tag}&ordering={ordering}&page_size=25')

# Parse the JSON response
data = response.json()
games_info = data['results']

# Connect to the SQLite database
conn = sqlite3.connect('games_database.db')

# Create a cursor object
cursor = conn.cursor()

# Create table
cursor.execute('''CREATE TABLE IF NOT EXISTS MOBA_Games
                  (Id INT, Name TEXT, Rating REAL, Playtime INT)''')

# Insert the games' information into the database
for game_info in games_info:
    cursor.execute("SELECT * FROM MOBA_Games WHERE Id = ?", (game_info['id'],))
    game_in_db = cursor.fetchone()
    if game_in_db is None:
        cursor.execute("INSERT INTO MOBA_Games (Id, Name, Rating, Playtime) VALUES (?, ?, ?, ?)",
                       (game_info['id'], game_info['name'], game_info['rating'], game_info['playtime']))
# Commit the changes
conn.commit()

# Close the connection
conn.close()