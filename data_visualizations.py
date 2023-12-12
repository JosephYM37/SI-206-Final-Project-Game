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