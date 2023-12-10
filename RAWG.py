import unittest
import sqlite3
import json
import os
import matplotlib.pyplot as plt
import requests

api_key = "34cf19bf45874c2c9d0ed8defa498b17"
api_url = f"https://api.rawg.io/api/games"
api_url = api_url + '?key=' + api_key

game_name = 'League of Legends'

response = requests.get(f'{api_url}&search={game_name}')
 
data = response.json()
game_info = data['results'][0]

conn = sqlite3.connect('games_database.db')

cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS League_of_Legends
                  (Id INT, Name TEXT, Rating REAL, Playtime INT)''')

cursor.execute("INSERT INTO League_of_Legends (id, name, rating, playtime) VALUES (?, ?, ?, ?)",
               (game_info['id'], game_info['name'], game_info['rating'], game_info['playtime']))
conn.commit()
conn.close()