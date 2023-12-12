# Robin Jiao, Shawn Rao, Joseph Chen
# To visualize: average time spent between games, difference between pro level and normal engagement
import sqlite3
import requests
import matplotlib.pyplot as plt

conn = sqlite3.connect('your_database.db')
cursor = conn.cursor()