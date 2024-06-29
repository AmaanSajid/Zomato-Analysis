import csv
import sqlite3
import chardet

# Database file path
db_file = 'zomato_database.db'

# CSV file path - replace with the actual path to your Zomato CSV file
csv_file = 'Data\zomato.csv'

# Function to detect file encoding
def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
    return chardet.detect(raw_data)['encoding']

# Create a connection to the database
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Detect file encoding
file_encoding = detect_encoding(csv_file)
print(f"Detected file encoding: {file_encoding}")

# If encoding detection fails, use a fallback encoding
if not file_encoding:
    file_encoding = 'iso-8859-1'
    print(f"Encoding detection failed. Using fallback encoding: {file_encoding}")

# Read CSV and insert data into the database
skipped_rows = 0
inserted_rows = 0

try:
    with open(csv_file, 'r', encoding=file_encoding) as file:
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            try:
                cursor.execute('''
                INSERT INTO zomato_restaurants (
                    Restaurant_ID, Restaurant_Name, Country_Code, City, Address, 
                    Locality, Locality_Verbose, Longitude, Latitude, Cuisines, 
                    Average_Cost_for_two, Currency, Has_Table_booking, Has_Online_delivery, 
                    Is_delivering_now, Switch_to_order_menu, Price_range, Aggregate_rating, 
                    Rating_color, Rating_text, Votes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    int(row['Restaurant ID']),
                    row['Restaurant Name'],
                    int(row['Country Code']),
                    row['City'],
                    row['Address'],
                    row['Locality'],
                    row['Locality Verbose'],
                    float(row['Longitude']),
                    float(row['Latitude']),
                    row['Cuisines'],
                    float(row['Average Cost for two']),
                    row['Currency'],
                    row['Has Table booking'],  # Changed from int() to string
                    row['Has Online delivery'],  # Changed from int() to string
                    row['Is delivering now'],  # Changed from int() to string
                    row['Switch to order menu'],  # Changed from int() to string
                    int(row['Price range']),
                    float(row['Aggregate rating']),
                    row['Rating color'],
                    row['Rating text'],
                    int(row['Votes'])
                ))
                inserted_rows += 1
            except Exception as e:
                print(f"Error inserting row: {e}")
                skipped_rows += 1
                continue

    # Commit changes and close connection
    conn.commit()
    print(f"Data loading completed. Inserted rows: {inserted_rows}, Skipped rows: {skipped_rows}")

except Exception as e:
    print(f"An error occurred: {e}")
    conn.rollback()

finally:
    conn.close()