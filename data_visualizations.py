# Robin Jiao, Shawn Rao, Joseph Chen
# To visualize: average time spent between games, difference between pro level and normal engagement
import sqlite3
import requests
import matplotlib.pyplot as plt

conn = sqlite3.connect('games_database.db')
cursor = conn.cursor()

cursor.execute("SELECT Playtime FROM JoinedData WHERE Name = 'League of Legends'")
lol_playtimes = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT Playtime FROM JoinedData WHERE Name = 'Dota2'")
dota2_playtimes = [row[0] for row in cursor.fetchall()]

playtimes = lol_playtimes + dota2_playtimes
plt.bar(['League of Legends', 'Dota2'], playtimes)
plt.xlabel('Game')
plt.ylabel('Average Playtime (hours)')
plt.title('Average Playtimes of League of Legends and Dota2')
plt.show()