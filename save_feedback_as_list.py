import sqlite3

# Path to your database file
db_path = 'feedback.db'

# Function to fetch data from the database and relabel columns
def fetch_feedback_data(db_path):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Get table name dynamically if unknown (optional)
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        table_name = tables[0][0]  # Assuming the first table contains the data

        # Query all data from the table
        cursor.execute(f"SELECT * FROM {table_name};")
        rows = cursor.fetchall()

        # Relabel columns as "ID" and "Consumer Feedback"
        feedback_list = [{"ID": row[0], "Consumer Feedback": row[1]} for row in rows]

        # Close the connection
        conn.close()

        return feedback_list

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []

# Call the function and display the feedback
feedback_data = fetch_feedback_data(db_path)
print(feedback_data)
