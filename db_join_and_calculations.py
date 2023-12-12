import sqlite3
from datetime import timedelta

# Connect to the database
conn = sqlite3.connect('games_database.db')
cursor = conn.cursor()

# Execute the SQL query to join tables and create a new table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS JoinedData AS
    SELECT GameNames.ID, GameNames.Name, GamePlaytimes.Playtime
    FROM GameNames
    JOIN GamePlaytimes ON GameNames.ID = GamePlaytimes.ID
''')

# Commit changes to the database
conn.commit()
conn.close()

# Connect to the database
conn = sqlite3.connect('games_database.db')
cursor = conn.cursor()

try:
    # Fetch the average game duration from the Faker_matches table
    cursor.execute("SELECT AVG(game_duration) FROM Faker_matches")
    average_game_duration = cursor.fetchone()[0]
    
    print(f"Average game duration for League of Legends: {average_game_duration} minutes")
    
    # Fetch the total playtime for League of Legends from the Game Playtimes table
    cursor.execute("SELECT SUM(playtime) FROM JoinedData WHERE name = 'League of Legends'")
    total_playtime = cursor.fetchone()[0]
    
    print(f"Total playtime for League of Legends: {total_playtime} hours")
    
    # Calculate the average number of games played
    average_number_of_games = (total_playtime * 60) // average_game_duration
    print("total_playtime * 60) / average_game_duration")
    print("         (* 60 to convert hours to minutes)")
    
    print(f"Average number of games played: {average_number_of_games}")
    
except sqlite3.Error as e:
    print("Error reading data from the database:", e)

# Close the connection
conn.close()



conn = sqlite3.connect('games_database.db')
cursor = conn.cursor()

# Query to retrieve game durations and k/d/a from the Faker_matches table
cursor.execute("SELECT Game_Duration, Kills, Deaths, Assists FROM Faker_matches")
games = cursor.fetchall()

# Initialize counters for different time slots and corresponding k/d/a values
time_slots = {'< 10': [], '10 - 20': [], '20 - 30': [], '30 - 40': [], '40+': []}

# Iterate through the games and categorize based on duration
for game in games:
    time_parts = game[0].split(':')  # Split the time into hours and minutes
    duration = int(time_parts[0]) + int(time_parts[1])  # Convert time to minutes
    
    # Calculate k/d/a
    kills = game[1]
    deaths = game[2]
    assists = game[3]
    
    kda = (kills + assists) / deaths if deaths != 0 else 0  # Calculate k/d/a

    if duration < 10:
        time_slots['< 10'].append(kda)
    elif 10 <= duration < 20:
        time_slots['10 - 20'].append(kda)
    elif 20 <= duration < 30:
        time_slots['20 - 30'].append(kda)
    elif 30 <= duration < 40:
        time_slots['30 - 40'].append(kda)
    else:
        time_slots['40+'].append(kda)

# Calculate average k/d/a for each time slot
average_kda = {}
for slot, kd_values in time_slots.items():
    if kd_values:
        average_kda[slot] = sum(kd_values) / len(kd_values)
    else:
        average_kda[slot] = 0

# Display the relationship between time and k/d/a
print("\nTime Slot    Average K/D/A")
for slot, avg_kda in average_kda.items():
    print(f"{slot:<12} {avg_kda:.2f}")

# Close the connection
conn.close()


