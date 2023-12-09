import unittest
import sqlite3
import json
import os
import matplotlib.pyplot as plt
import requests

api_key = "RGAPI-5ccc7cc0-ad7d-4fe3-b577-2f46a827bbc4"
api_url = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/MonkyPeen"
api_url = api_url + '?api_key=' + api_key

resp = requests.get(api_url)
player_info = resp.json()
print(player_info)

api_url_match = "https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/irE6cW5IhU_qNdil0T9Fy7G44rhZAWvy85UTOsf6R3bGv3A-_TXDqxKQZiIUGZe9oynKIHfgF5VTMg/ids?start=0&count=20"
api_url_match = api_url_match + '&api_key=' + api_key 
resp = requests.get(api_url_match)
match_ids = resp.json()
print(match_ids)

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
