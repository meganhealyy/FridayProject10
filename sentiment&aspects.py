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

# Expanded list of predefined aspects with broader terms and synonyms
relevant_aspects = [
    'quality', 'price', 'usability', 'design', 'performance', 'features', 'material', 'ease of use', 
    'customer service', 'customer support', 'durability', 'size', 'comfort', 'battery life', 'sound', 
    'speed', 'value', 'aesthetics', 'packaging', 'battery', 'price range', 'look', 'functionality', 
    'build quality', 'weight', 'texture', 'sturdiness', 'lag', 'high-demand', 'integration', 
    'productivity', 'navigation', 'eye-tracking', 'technology', 'shipping', 'returns', 'warranty', 
    'setup', 'instructions', 'compatibility', 'connectivity', 'availability', 'support', 'visuals', 
    'hardware', 'user-friendly', 'glitches', 'software', 'simplicity', 'expensive', 'display', 'interact', 'resolution',
    'controls', 'perform', 'Apple services', 'usefulness'
]

# Normalization dictionary for broader aspect matching
aspect_normalization = {
    "battery life": "battery",
    "battery": "battery",
    "price range": "price",
    "speed": "performance",
    "durability": "build quality",
    "weight": "design",
    "aesthetics": "design",
    "functionality": "features",
    "features": "features",
    "eye-tracking": "technology",
    "integration": "technology",
    "usability": "ease of use",
    "ease of use": "ease of use",
    "performance": "performance",
    "lag": "performance",
    "navigation": "technology",
    "technology": "technology",
    "customer support": "customer service",
    "customer service": "customer service",
    "shipping": "shipping",
    "returns": "returns",
    "warranty": "warranty",
    "setup": "setup",
    "instructions": "setup",
    "compatibility": "compatibility",
    "connectivity": "compatibility",
    "availability": "availability",
    "support": "customer service",
    "visuals": "visuals",
    "hardware": "hardware",
    "user-friendly": "ease of use",
    "glitches": "performance",
    "software": "technology",
    "simplicity": "ease of use",
    "expensive": "price",
    "display": "display",
    "interact": "interaction",
    "resolution": "display",
    "controls": "usability",
    "perform": "performance",
    "Apple services": "technology",
    "usefulness": "usability"
}

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

# Function to extract relevant aspects and normalize
def extract_aspects(feedback):
    # Convert the feedback to lowercase
    feedback = feedback.lower()

    # List to store matched aspects
    matched_aspects = []

    # Loop through each predefined aspect and check if it's mentioned in the review
    for aspect in relevant_aspects:
        if aspect in feedback:
            normalized_aspect = aspect_normalization.get(aspect, aspect)
            matched_aspects.append(normalized_aspect)

    # Remove duplicates while preserving order
    matched_aspects = list(dict.fromkeys(matched_aspects))

    # Limit to a maximum of 3 aspects
    return matched_aspects[:3]

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

# Extract individual aspects into separate columns (Aspect 1, Aspect 2, Aspect 3)
feedback_df['Aspect 1'] = feedback_df['Aspects'].apply(lambda x: x.split(', ')[0] if x else None)
feedback_df['Aspect 2'] = feedback_df['Aspects'].apply(lambda x: x.split(', ')[1] if len(x.split(', ')) > 1 else None)
feedback_df['Aspect 3'] = feedback_df['Aspects'].apply(lambda x: x.split(', ')[2] if len(x.split(', ')) > 2 else None)

# Save the DataFrame to an Excel file
feedback_df.to_excel(output_excel_file, index=False)

print(f"Data with sentiment and aspects saved to {output_excel_file}")
