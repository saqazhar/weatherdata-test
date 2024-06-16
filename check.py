import sqlite3

# Step 1: Connect to the database
conn = sqlite3.connect('app.db')  # replace 'example.db' with your database file

# Step 2: Create a cursor object
cursor = conn.cursor()

# Step 3: Execute a query
cursor.execute('SELECT * FROM weather_stations')  # replace 'table_name' with your table

# Step 4: Fetch the data
rows = cursor.fetchall()

# Step 5: Check the data
for row in rows:
    print(row)

# Step 6: Close the connection
conn.close()
