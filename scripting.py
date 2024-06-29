import sqlite3

# Connect to the database
conn = sqlite3.connect('zomato_database.db')
cursor = conn.cursor()

# Add the new Country column
cursor.execute("ALTER TABLE zomato_restaurants ADD COLUMN Country TEXT;")

# Define the country code to country name mapping
country_mapping = {
    1: 'India',
    14: 'Australia',
    30: 'Brazil',
    37: 'Canada',
    94: 'Indonesia',
    148: 'New Zealand',
    162: 'Philippines',
    166: 'Qatar',
    184: 'Singapore',
    189: 'South Africa',
    191: 'Sri Lanka',
    208: 'Turkey',
    214: 'UAE',
    215: 'United Kingdom',
    216: 'United States'
}

# Update the Country column based on the Country Code
for code, country in country_mapping.items():
    cursor.execute("""
    UPDATE zomato_restaurants
    SET Country = ?
    WHERE Country_Code = ?
    """, (country, code))

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Country column added and updated successfully.")


#checking the addition for country code and country name.

# Query to check the results
# cursor.execute("""
# SELECT DISTINCT Country_Code, Country
# FROM zomato_restaurants
# ORDER BY Country_Code;
# """)

# results = cursor.fetchall()

# for row in results:
#     print(f"Country Code: {row[0]}, Country: {row[1]}")

# conn.close()
