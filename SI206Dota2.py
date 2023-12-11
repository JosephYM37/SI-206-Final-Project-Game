import requests
import json
import unittest
import os

###########################################
# Your name:Shawn Rao                     #
# Who you worked with: Robin, Joseph      #
###########################################

#rl = "https://rawg-video-games-database.p.rapidapi.com/games/%7Bgame_pk%7D"
api_key = '493c3ffc77b743689ceb65d56fd0975e'
base_url = 'https://rawg-video-games-database.p.rapidapi.com/games'

headers = {
    'x-rapidapi-key': "e6ef05302emsh9c46dd59d7ac5d1p13a2d8jsneb37aae7d452",
    'x-rapidapi-host': "rawg-video-games-database.p.rapidapi.com"
}

def get_game_info(game_name):
    params = {
        'key': api_key,
        'search': game_name,
        'page_size': 1,  # Limit to 1 result for simplicity, adjust as needed
        'additions': 'game,players,stats,stores,platforms,metacritic,reddit,twitch,creator,collections,genres'  # Include additional details
    }

    try:
        response = requests.get(base_url, headers=headers, params=params)
        response.raise_for_status()

        data = response.json()

        if 'results' in data:
            games = data['results']

            if games:
                game = games[0]
                print(f"Name: {game.get('name', 'N/A')}")
                print(f"Released: {game.get('released', 'N/A')}")
                print(f"Metacritic Score: {game.get('metacritic', 'N/A')}")

                # Additional details
                print(f"Background Image: {game.get('background_image', 'N/A')}")
                print(f"Genres: {', '.join(genre['name'] for genre in game.get('genres', []))}")

                # Player details
                print(f"Players: {game.get('playtime', 'N/A')}")

                # Global stats
                print(f"Ratings: {game.get('ratings_count', 'N/A')}")
                print(f"Avg. Rating: {game.get('rating', 'N/A')}")

                # Store details
                stores = game.get('stores', [])
                if stores:
                    print("Stores:")
                    for store in stores:
                        print(f" - {store.get('store', {}).get('name', 'N/A')}")

                # Platform details
                platforms = game.get('platforms', [])
                if platforms:
                    print("Platforms:")
                    for platform in platforms:
                        print(f" - {platform.get('platform', {}).get('name', 'N/A')}")

                # Additional details for popularity, copies bought, active player count, etc.
                added_info = game.get('added', {})
                if isinstance(added_info, dict):
                    print(f"Copies Bought: {added_info.get('owned', 'N/A')}")
                    print(f"Active Players: {added_info.get('playing', 'N/A')}")
                else:
                    print("Unable to retrieve copies bought and active player count.")

                print(f"Popularity: {game.get('popularity', 'N/A')}")
                print(f"Reddit Mentions: {game.get('reddit', {}).get('count', 'N/A')}")
                print(f"Twitch Views: {game.get('twitch', {}).get('count', 'N/A')}")

                # Add more details as needed
            else:
                print(f"No results found for {game_name}")
        else:
            print("Unexpected response format")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    game_name = input("Enter the name of the game: ")
    get_game_info(game_name)


