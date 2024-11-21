import sqlite3
import pandas as pd

# Path to your database file
db_path = 'feedback.db'
output_excel_file = 'customer_feedback.xlsx'  # Name of the Excel file to save

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

# Fetch feedback data
feedback_data = fetch_feedback_data(db_path)

# Convert the list of dictionaries to a pandas DataFrame
feedback_df = pd.DataFrame(feedback_data)

# Save the DataFrame to an Excel file
feedback_df.to_excel(output_excel_file, index=False)

print(f"Data saved to {output_excel_file}")
