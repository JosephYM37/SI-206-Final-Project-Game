import json
import sqlite3
import requests

api_key = "RGAPI-62a08042-f71c-447a-a838-dda03f1df511"
region = 'ASIA'
puuid = 'vtIfRD_OKhXlZHUeqLka5ImRnpV3uyKIqkpwpvGKbmPcuhcsVBcs92WnmxaiHDYLFb1m66bHxuUaKg'


api_url = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/Hide%20on%20Bush"
requests.get(api_url)

api_url = api_url + '?api_key=' + api_key

resp = requests.get(api_url)
player_info = resp.json()


api_match_url = "https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/vtIfRD_OKhXlZHUeqLka5ImRnpV3uyKIqkpwpvGKbmPcuhcsVBcs92WnmxaiHDYLFb1m66bHxuUaKg/ids?start=0&count=20"
requests.get(api_match_url)
api_match_url = api_match_url + '&api_key=' + api_key
resp = requests.get(api_match_url)
matches = resp.json()

api_match1_url = "https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/vtIfRD_OKhXlZHUeqLka5ImRnpV3uyKIqkpwpvGKbmPcuhcsVBcs92WnmxaiHDYLFb1m66bHxuUaKg/ids?start=21&count=20"
requests.get(api_match1_url)
api_match1_url = api_match1_url + '&api_key=' + api_key
resp = requests.get(api_match1_url)
matches0 = resp.json()

api_match2_url = "https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/vtIfRD_OKhXlZHUeqLka5ImRnpV3uyKIqkpwpvGKbmPcuhcsVBcs92WnmxaiHDYLFb1m66bHxuUaKg/ids?start=41&count=20"
requests.get(api_match2_url)
api_match2_url = api_match2_url + '&api_key=' + api_key
resp = requests.get(api_match2_url)
matches1 = resp.json()

api_match3_url = "https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/vtIfRD_OKhXlZHUeqLka5ImRnpV3uyKIqkpwpvGKbmPcuhcsVBcs92WnmxaiHDYLFb1m66bHxuUaKg/ids?start=61&count=20"
requests.get(api_match3_url)
api_match3_url = api_match3_url + '&api_key=' + api_key
resp = requests.get(api_match3_url)
matches2 = resp.json()

api_match4_url = "https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/vtIfRD_OKhXlZHUeqLka5ImRnpV3uyKIqkpwpvGKbmPcuhcsVBcs92WnmxaiHDYLFb1m66bHxuUaKg/ids?start=81&count=20"
requests.get(api_match4_url)
api_match4_url = api_match4_url + '&api_key=' + api_key
resp = requests.get(api_match4_url)
matches3 = resp.json()

def get_match_data(region, match_id, api_key):
    api_url = (
        "https://" +
        region +
        ".api.riotgames.com/lol/match/v5/matches/" +
        match_id +
        "?api_key=" +
        api_key
    )
    resp = requests.get(api_url)
    data = resp.json()
    return data

def did_win(puuid, match_data):
    part_index = match_data['metadata']['participants'].index(puuid)
    return match_data['info']['participants'][part_index]['win']

def game_duration(match_data):
    return match_data['info']['gameDuration']

def get_champion(puuid, match_data):
    part_index = match_data['metadata']['participants'].index(puuid)
    return match_data['info']['participants'][part_index]['championName']

def get_kill(puuid, match_data):
    part_index = match_data['metadata']['participants'].index(puuid)
    return match_data['info']['participants'][part_index]['kills']

def get_death(puuid, match_data):
    part_index = match_data['metadata']['participants'].index(puuid)
    return match_data['info']['participants'][part_index]['deaths']

def get_assist(puuid, match_data):
    part_index = match_data['metadata']['participants'].index(puuid)
    return match_data['info']['participants'][part_index]['assists']

match_id_to_check1 = "KR_6823337832" # match 0-20
match_id_to_check2 = "KR_6800509589" # match 21-40
match_id_to_check3 = "KR_6793066935" # match 41-60
match_id_to_check4 = "KR_6789837280" # match 61-80

conn = sqlite3.connect('games_database.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS Faker_matches
                  (Match_ID TEXT PRIMARY KEY,
                  Game_Duration INT, 
                  Champion TEXT, 
                  Kills INT, 
                  Deaths INT, 
                  Assists INT, 
                  Victory TEXT)''')

if cursor.execute("SELECT COUNT(*) FROM Faker_matches WHERE match_id = ?", (match_id_to_check4,)).fetchone()[0] > 0:
    mat = matches3
elif cursor.execute("SELECT COUNT(*) FROM Faker_matches WHERE match_id = ?", (match_id_to_check3,)).fetchone()[0] > 0:
    mat = matches2
elif cursor.execute("SELECT COUNT(*) FROM Faker_matches WHERE match_id = ?", (match_id_to_check2,)).fetchone()[0] > 0:
    mat = matches1
elif cursor.execute("SELECT COUNT(*) FROM Faker_matches WHERE match_id = ?", (match_id_to_check1,)).fetchone()[0] > 0:
    mat = matches0
else:
    mat = matches

for match_id in mat:
    match_data = get_match_data(region, match_id, api_key)
    # Extract relevant data
    total_seconds = game_duration(match_data)
    minutes, seconds = divmod(total_seconds, 60)
    time_format = "{:02d}:{:02d}".format(int(minutes), int(seconds))
    
    champion_val = get_champion(puuid, match_data)
    kill_val = get_kill(puuid, match_data)
    death_val = get_death(puuid, match_data)
    assist_val = get_assist(puuid, match_data)
    victory_val = did_win(puuid, match_data)

    # Insert the match data into the database table
    cursor.execute('''INSERT OR IGNORE INTO Faker_matches 
                    (Match_ID, Game_Duration, Champion, Kills, Deaths, Assists, Victory) 
                    VALUES (?, ?, ?, ?, ?, ?, ?)''',
                (match_id, time_format, champion_val, kill_val, death_val, assist_val, victory_val))

# Commit changes and close the connection after the loop
conn.commit()
conn.close()
