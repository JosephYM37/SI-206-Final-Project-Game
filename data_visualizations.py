# Robin Jiao, Shawn Rao, Joseph Chen
# To calculate: average time spent between games, difference between pro level and normal engagement
import sqlite3
import requests

conn = sqlite3.connect('games_database.db')
cursor = conn.cursor()
cursor.execute('''
    SELECT GameNames.Name, GamePlaytimes.Playtime
    FROM GameNames
    JOIN GamePlaytimes ON GameNames.Id = GamePlaytimes.Id
''')
results = cursor.fetchall()
total_playtime = sum(row[1] for row in results)
average_playtime = total_playtime / len(results)
with open('average_playtime.txt', 'w') as f:
    f.write(f'Average playtime: {average_playtime}\n')