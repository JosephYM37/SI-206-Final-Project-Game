import requests
import json
import unittest
import os

###########################################
# Your name:Shawn Rao                     #
# Who you worked with: Robin, Joseph      #
###########################################

# list of actual endpoint URLs provided by the API
api_endpoints = ['https://api.opendota.com/api/matches/3703866531', 'https://api.opendota.com/api/playersByRank', 'https://api.opendota.com/api/rankings']#, 'URL2', 'URL3']

#  'params' dictionary
params = {
    'param1': 'value1',
    'param2': 'value2',
    # Add more parameters as needed
}

try:
    for api_endpoint in api_endpoints:
        # GET request to each API endpoint
        response = requests.get(api_endpoint, params=params)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Print or process data as needed
            print(f"Data from {api_endpoint}:")
            print(data)
            print("\n" + "="*50 + "\n")
        else:
            print(f"Error: {response.status_code} - {response.text} for {api_endpoint}")

except requests.exceptions.RequestException as e:
    print(f"Error: {e}")