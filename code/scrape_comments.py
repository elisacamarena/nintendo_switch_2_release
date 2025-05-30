"""Fetch comments from a YouTube video using YouTube Data API v3

This script creates a database from the last 1,000 comments from Nintendo's Switch 2 console release video. The data is then processed to 
classify the comments into "positive", "neutral" and "negative" to analyse the potential consumers' sentiment before the console's launch date.
"""

# Imports
import os
import csv
from dotenv import load_dotenv
from googleapiclient.discovery import build
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt

# Load API key from .env
load_dotenv()
key = os.getenv('API_KEY')

# Build YouTube API client
youtube = build('youtube', 'v3', developerKey=key)

# --- CONFIGURATION ---

# 🔗 Paste your full YouTube video URL here:
video_url = "https://www.youtube.com/watch?v=9flte56erE8"

# Extract video ID from URL 
video_id = video_url.split("v=")[-1].split("&")[0]

# Set number of comments to analyze
TARGET_COMMENT_COUNT = 1000
COMMENTS_PER_PAGE = 100  # max allowed by API

# --- FETCH COMMENTS ---

comments = []
next_page_token = None

while len(comments) < TARGET_COMMENT_COUNT:
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=COMMENTS_PER_PAGE,
        pageToken=next_page_token,
        textFormat="plainText"
    )
    
    response = request.execute()
    
    for item in response["items"]:
        comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        username=item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"] 
        #X = item["snippet"]["topLevelComment"]["snippet"].keys()
        comments.append({"text":comment,"author":username})
        if len(comments) >= TARGET_COMMENT_COUNT:
            break

    # Check if there's another page
    next_page_token = response.get("nextPageToken")
    if not next_page_token:
        break  # No more comments

# --- SAVE TO CSV ---
# Ensure the data folder exists
os.makedirs("data", exist_ok=True)

csv_file_path = os.path.join("data", "comments.csv")

with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["author","text"])
    writer.writeheader()
    writer.writerows(comments)

## Load your CSV (adjust the path if needed)
df = pd.read_csv('data/comments.csv')  # or wherever your CSV is

# Function to classify sentiment
def classify_sentiment(text):
    blob = TextBlob(str(text))
    polarity = blob.sentiment.polarity
    return 'positive' if polarity > 0 else 'negative'

# Apply sentiment classification
df['sentiment'] = df['text'].apply(classify_sentiment)

# Count results
sentiment_counts = df['sentiment'].value_counts()
total = sentiment_counts.sum()

# Calculate percentage
percentages = (sentiment_counts / total) * 100

print(percentages)

plt.figure(figsize=(6, 6))
colors = ['#4CAF50', '#F44336']  # Green, Red
percentages.plot.pie(
    autopct='%1.1f%%',
    startangle=90,
    colors=colors,
    labels=['Positive', 'Negative']
)

plt.title('Sentiment Analysis of Nintendo Switch 2 release video')
plt.ylabel('')
plt.tight_layout()
plt.show()