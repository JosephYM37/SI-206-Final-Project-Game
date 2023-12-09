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
