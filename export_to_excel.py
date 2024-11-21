import sqlite3
import pandas as pd
import openai
from dotenv import load_dotenv
import os
import time

# Load environment variables from the .env file
load_dotenv()

# Retrieve the OpenAI API key from environment variables
openai.api_key = os.getenv("key")

# Ensure the API key is loaded correctly
if openai.api_key is None:
    print("Error: OPENAI_API_KEY not found in .env file")
    exit()

# Path to your database file
db_path = 'feedback.db'
output_excel_file = 'customer_feedback_with_sentiment_and_aspects.xlsx'  # Name of the Excel file to save

# Expanded list of predefined aspects
# Expanded list of predefined aspects with new additions
relevant_aspects = [
    'quality', 'price', 'usability', 'design', 'performance', 'features', 'material', 'ease of use', 
    'customer service', 'durability', 'size', 'comfort', 'battery life', 'sound', 'speed', 'value', 
    'aesthetics', 'packaging', 'battery', 'price range', 'look', 'functionality', 'build quality', 'weight', 
    'texture', 'sturdiness', 'lag', 'high-demand', 'integration', 'productivity', 
    'navigation', 'eye-tracking', 'technology'
]

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

# Function to analyze sentiment using OpenAI's API with retry logic
def analyze_sentiment(feedback):
    attempt = 0
    while attempt < 3:
        try:
            # Send the feedback to OpenAI's API for sentiment analysis
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # You can also try "gpt-4"
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": f"Classify the sentiment of this review as 'Positive', 'Negative', or 'Neutral':\n\n{feedback}"}
                ],
                max_tokens=60,
                temperature=0.3,  # Low temperature for more predictable responses
                timeout=30  # Set a timeout for the request
            )

            sentiment = response['choices'][0]['message']['content'].strip()
            
            # Log the raw response to check the exact output for better analysis
            print(f"Raw response: {sentiment}")

            # Classification based on detected sentiment
            if 'positive' in sentiment.lower():
                return "Positive"
            elif 'negative' in sentiment.lower():
                return "Negative"
            elif 'neutral' in sentiment.lower() or 'mixed' in sentiment.lower():
                return "Neutral"
            else:
                return "Neutral"  # Default to Neutral if unsure

        except openai.error.OpenAIError as e:
            # Catch OpenAI-specific errors
            print(f"OpenAI API Error: {e}")
            time.sleep(5)  # Wait before retrying
            attempt += 1
        except Exception as e:
            # Catch other unexpected errors
            print(f"General Error: {e}")
            time.sleep(5)  # Wait before retrying
            attempt += 1

    return "Neutral"  # Default to Neutral after 3 attempts

# Function to extract relevant aspects from the review text by checking for keyword matches
def extract_aspects(feedback):
    # Convert the feedback to lowercase
    feedback = feedback.lower()

    # List to store matched aspects
    matched_aspects = []

    # Loop through each predefined aspect and check if it's mentioned in the review
    for aspect in relevant_aspects:
        if aspect in feedback:
            matched_aspects.append(aspect)

    # Remove duplicates (check if the aspect is already in the list)
    matched_aspects = list(set(matched_aspects))  # Remove any duplicates

    return matched_aspects

# Fetch feedback data
feedback_data = fetch_feedback_data(db_path)

# Process the feedback in batches (e.g., 10 at a time)
batch_size = 10
for i in range(0, len(feedback_data), batch_size):
    batch = feedback_data[i:i + batch_size]
    
    for feedback in batch:
        sentiment = analyze_sentiment(feedback["Consumer Feedback"])
        aspects = extract_aspects(feedback["Consumer Feedback"])
        
        feedback["Sentiment"] = sentiment
        feedback["Aspects"] = ', '.join(aspects)  # Combine aspects into a string for easy viewing
        
        print(f"Processed feedback ID {feedback['ID']} - Sentiment: {sentiment}, Aspects: {', '.join(aspects)}")

# Convert the list of dictionaries to a pandas DataFrame
feedback_df = pd.DataFrame(feedback_data)

# Extract individual aspects into separate columns (Aspect 1, Aspect 2, Aspect 3, etc.)
feedback_df['Aspect 1'] = [aspect.split(',')[0] if len(aspect.split(',')) > 0 else None for aspect in feedback_df['Aspects']]
feedback_df['Aspect 2'] = [aspect.split(',')[1] if len(aspect.split(',')) > 1 else None for aspect in feedback_df['Aspects']]
feedback_df['Aspect 3'] = [aspect.split(',')[2] if len(aspect.split(',')) > 2 else None for aspect in feedback_df['Aspects']]

# Save the DataFrame to an Excel file
feedback_df.to_excel(output_excel_file, index=False)

print(f"Data with sentiment and aspects saved to {output_excel_file}")
