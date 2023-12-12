import requests

#################################################
# Your name:Shawn Rao                           #
# Who you worked with: Robin Jiao, Joseph Chen  # 
# API Used: Rapid API/RAWG API                  #
#################################################

#api key needed to access API data
api_key = '493c3ffc77b743689ceb65d56fd0975e'

#url for RAWG and RapidAPi api data access
base_url = 'https://rawg-video-games-database.p.rapidapi.com/games'
headers = {
    'x-rapidapi-key': "e6ef05302emsh9c46dd59d7ac5d1p13a2d8jsneb37aae7d452",
    'x-rapidapi-host': "rawg-video-games-database.p.rapidapi.com"
}

#set parameters
def get_api_response(game_name):
    params = {
        'key': api_key,
        'search': game_name,
        'page_size': 1,
        'additions': 'game,players,stats,stores,platforms,metacritic,reddit,twitch,creator,collections,genres'  # Include additional details
    }

    #error handling
    try:
        response = requests.get(base_url, headers=headers, params=params)
        response.raise_for_status()

        data = response.json()
        return data

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")


#output statements
def print_game_details(game):
    print(f"Name: {game.get('name', 'N/A')}")
    print(f"Released: {game.get('released', 'N/A')}")
    print(f"Metacritic Score: {game.get('metacritic', 'N/A')}")
    print(f"Background Image: {game.get('background_image', 'N/A')}")
    print(f"Genres: {', '.join(genre['name'] for genre in game.get('genres', []))}")
    print(f"Players: {game.get('playtime', 'N/A')}")
    print(f"Ratings: {game.get('ratings_count', 'N/A')}")
    print(f"Avg. Rating: {game.get('rating', 'N/A')}")

    stores = game.get('stores', [])
    if stores:
        print("Stores:")
        for store in stores:
            print(f" - {store.get('store', {}).get('name', 'N/A')}")

    platforms = game.get('platforms', [])
    if platforms:
        print("Platforms:")
        for platform in platforms:
            print(f" - {platform.get('platform', {}).get('name', 'N/A')}")

    added_info = game.get('added', {})
    if isinstance(added_info, dict):
        print(f"Copies Bought: {added_info.get('owned', 'N/A')}")
        print(f"Active Players: {added_info.get('playing', 'N/A')}")
    else:
        print("Unable to retrieve copies bought and active player count.")

    print(f"Popularity: {game.get('popularity', 'N/A')}")
    print(f"Reddit Mentions: {game.get('reddit', {}).get('count', 'N/A')}")
    print(f"Twitch Views: {game.get('twitch', {}).get('count', 'N/A')}")

# access the api data
def get_game_info(game_name):
    data = get_api_response(game_name)

    if 'results' in data:
        games = data['results']

        if games:
            game = games[0]
            print_game_details(game)
        else:
            print(f"No results found for {game_name}")
    else:
        print("Unexpected response format")

# ask for game
if __name__ == '__main__':
    game_name = input("Enter the name of the game: ")
    get_game_info(game_name)

