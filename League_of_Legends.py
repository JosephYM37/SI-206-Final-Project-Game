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

<<<<<<< HEAD
# Insert data into the table
for player in data['players']:
    cursor.execute("INSERT INTO Players (Name, Rank, LP) VALUES (?, ?, ?)",
                   (player['name'], player['rank'], player['lp']))

# Commit changes and close connection
conn.commit()
conn.close()

print("Data inserted into SQLite database.")
=======
api_url_matchid = "https://americas.api.riotgames.com/lol/match/v5/matches/NA1_4836852673"

api_url_matchid = api_url_matchid + '?api_key=' + api_key
resp = requests.get(api_url_matchid)
match_data = resp.json()


player_data = match_data['info']['participants'][0]
k = player_data['kills']
d = player_data['deaths']
a = player_data['assists']
print("Kills:", k)
print("Deaths:", d)
print("Assists:", a)
print("KDA:", (k + a) / d)
>>>>>>> refs/remotes/origin/main
