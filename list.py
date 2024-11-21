import sqlite3

# Replace 'your_database.db' with the path to your .db file
db_file = 'feedback.db'

# Connect to the database
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Fetch all rows from the 'feedback' table
cursor.execute("SELECT * FROM feedback;")
rows = cursor.fetchall()

# Convert rows into a list
feedback_list = [list(row) for row in rows]

# Close the connection
conn.close()

# Print a sample of the list
print(f"Total rows: {len(feedback_list)}")
for row in feedback_list[:80]:  
    print(row)
