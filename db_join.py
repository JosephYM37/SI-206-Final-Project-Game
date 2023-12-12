import sqlite3

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
