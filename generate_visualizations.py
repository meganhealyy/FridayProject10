import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the Excel file into a pandas DataFrame
excel_file = 'customer_feedback_with_sentiment_and_aspects.xlsx'
feedback_df = pd.read_excel(excel_file)

# Check the first few rows of the DataFrame to ensure it loaded correctly
print(feedback_df.head())

# Function to plot sentiment distribution
def plot_sentiment_distribution(df):
    sentiment_counts = df['Sentiment'].value_counts()
    sentiment_counts.plot(kind='bar', color=['green', 'red', 'gray'])
    plt.title('Sentiment Distribution')
    plt.xlabel('Sentiment')
    plt.ylabel('Frequency')
    plt.xticks(rotation=0)
    plt.show()

# Function to plot aspect frequency distribution
def plot_aspect_frequency(df):
    # Split the 'Aspects' column to get individual aspects
    aspects = df['Aspects'].dropna().str.split(', ', expand=True).stack()
    aspect_counts = aspects.value_counts()
    aspect_counts.plot(kind='bar', color='skyblue')
    plt.title('Aspect Frequency Distribution')
    plt.xlabel('Aspect')
    plt.ylabel('Frequency')
    plt.xticks(rotation=90)
    plt.show()

# Function to analyze aspect sentiment (this is optional)
def plot_aspect_sentiment_analysis(df):
    aspect_sentiment = df.groupby('Sentiment')['Aspects'].apply(lambda x: x.str.split(', ').explode().value_counts()).unstack(fill_value=0)
    aspect_sentiment.plot(kind='bar', stacked=True)
    plt.title('Aspect Sentiment Analysis')
    plt.xlabel('Sentiment')
    plt.ylabel('Frequency of Aspects')
    plt.xticks(rotation=0)
    plt.show()

# Call the functions to generate the visualizations
plot_sentiment_distribution(feedback_df)
plot_aspect_frequency(feedback_df)
plot_aspect_sentiment_analysis(feedback_df)
