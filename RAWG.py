import unittest
import sqlite3
import json
import os
import matplotlib.pyplot as plt
import requests

api_key = "34cf19bf45874c2c9d0ed8defa498b17"
api_url = "https://api.rawg.io/api/games"
api_url = api_url + '?key=' + api_key

resp = requests.get(api_url)

url = "https://rawg-video-games-database.p.rapidapi.com/games/league-of-legends"

headers = {
	"X-RapidAPI-Key": "bd83204c63msh395f771e02eb0ddp15ced2jsna2072c4e0f3e",
	"X-RapidAPI-Host": "rawg-video-games-database.p.rapidapi.com"
}

response = requests.get(url, headers=headers)

print(response.json())
