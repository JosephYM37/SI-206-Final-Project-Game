#Robin Jiao
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

# Create a table to store the current page number if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS PageInfo
                  (Info TEXT PRIMARY KEY, Value INT)''')

# Retrieve the current page number from the database
cursor.execute("SELECT Value FROM PageInfo WHERE Info = 'CurrentPage'")
row = cursor.fetchone()
if row is None:
    # If the current page number doesn't exist in the database, initialize it to 1
    current_page = 1
    cursor.execute("INSERT INTO PageInfo (Info, Value) VALUES ('CurrentPage', ?)", (current_page,))
else:
    current_page = row[0]

# Define the tag and ordering
tag = 'MOBA'
ordering = '-rating'

# Make the API request with the current page number
response = requests.get(f'{api_url}&tags={tag}&ordering={ordering}&page_size=25&page={current_page}')

# Parse the JSON response
data = response.json()
games_info = data['results']

# Create table
cursor.execute('''CREATE TABLE IF NOT EXISTS MOBA_Games
                  (Id INT, Name TEXT, Rating REAL, Playtime INT)''')

# Insert the games' information into the database
for game_info in games_info:
    cursor.execute("SELECT * FROM MOBA_Games WHERE Id = ?", (game_info['id'],))
    game_in_db = cursor.fetchone()
    if game_in_db is None:
        cursor.execute("INSERT INTO MOBA_Games (Id, Name, Metacritic, Rating, Playtime) VALUES (?, ?, ?, ?, ?)",
                       (game_info['id'], game_info['name'], game_info['metacritic'], game_info['rating'], game_info['playtime']))

# Increment the current page number and update it in the database
current_page += 1
cursor.execute("UPDATE PageInfo SET Value = ? WHERE Info = 'CurrentPage'", (current_page,))

# Commit the changes
conn.commit()

# Close the connection
conn.close()