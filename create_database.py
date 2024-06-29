import sqlite3

# Database file path
db_file = 'zomato_database.db'

# Create a connection to the database
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Create the Zomato restaurants table
cursor.execute('''
CREATE TABLE IF NOT EXISTS zomato_restaurants (
    Restaurant_ID INTEGER PRIMARY KEY,
    Restaurant_Name TEXT,
    Country_Code INTEGER,
    City TEXT,
    Address TEXT,
    Locality TEXT,
    Locality_Verbose TEXT,
    Longitude REAL,
    Latitude REAL,
    Cuisines TEXT,
    Average_Cost_for_two REAL,
    Currency TEXT,
    Has_Table_booking INTEGER,
    Has_Online_delivery INTEGER,
    Is_delivering_now INTEGER,
    Switch_to_order_menu INTEGER,
    Price_range INTEGER,
    Aggregate_rating REAL,
    Rating_color TEXT,
    Rating_text TEXT,
    Votes INTEGER
)
''')

# Commit changes and close connection
conn.commit()
conn.close()

print("Database and Zomato restaurants table have been created successfully.")