#Robin Jiao
import sqlite3
import matplotlib.pyplot as plt
import requests

api_key = "34cf19bf45874c2c9d0ed8defa498b17"
api_url = f"https://api.rawg.io/api/games"
api_url = api_url + '?key=' + api_key

# Function to get games info from API
def get_games_info(api_url, tag, ordering, page):
    # Make the API request with the current page number
    response = requests.get(f'{api_url}&tags={tag}&ordering={ordering}&page_size=25&page={page}')
    # Parse the JSON response
    data = response.json()
    # Return the 'results' field of the response, or an empty list if 'results' is not present
    return data.get('results', [])

# Function to update database with games info
def update_database(cursor, games_info):
    for game_info in games_info:
        # Insert the game name into the GameNames table if it doesn't exist
        cursor.execute("INSERT OR IGNORE INTO GameNames (Id, Name) VALUES (?, ?)",
                       (game_info['id'], game_info['name']))
        # Insert the game playtime into the GamePlaytimes table if it doesn't exist
        cursor.execute("INSERT OR IGNORE INTO GamePlaytimes (Id, Playtime) VALUES (?, ?)",
                       (game_info['id'], game_info['playtime']))

def main():
    api_url = 'https://api.rawg.io/api/games?key=YOUR_API_KEY'
    tag = 'MOBA'
    ordering = '-rating'

    conn = sqlite3.connect('games_database.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS PageInfo
                      (Info TEXT PRIMARY KEY, Value INT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS GameNames
                      (Id INT PRIMARY KEY, Name TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS GamePlaytimes
                      (Id INT PRIMARY KEY, Playtime INT)''')

    cursor.execute("SELECT Value FROM PageInfo WHERE Info = 'CurrentPage'")
    row = cursor.fetchone()
    current_page = row[0] if row else 1

    while True:
        games_info = get_games_info(api_url, tag, ordering, current_page)
        if not games_info:
            break

        update_database(cursor, games_info)

        current_page += 1
        cursor.execute("INSERT OR REPLACE INTO PageInfo (Info, Value) VALUES ('CurrentPage', ?)", (current_page,))

        # Break the loop after processing one page of results
        break

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
