from googleapiclient.discovery import build
from textblob import TextBlob

def read_asset_names(file_path):
    """Reads asset names from a file."""
    try:
        with open(file_path, 'r') as file:
            asset_names = file.read().splitlines()
        return asset_names
    except FileNotFoundError:
        print("Error: File not found. Please provide a valid file path.")
        return []

def iterate_and_split_names(name):
    """Splits the provided name into separate letters."""
    print(f"Name: {name}")
    print("Letters:", ', '.join(name))

def check_name_in_assets(asset_names, name):
    """Checks if the provided name exists in the asset list."""
    if name in asset_names:
        print(f"The name '{name}' exists in the assets file.")
        iterate_and_split_names(name)
    else:
        print(f"The name '{name}' does not exist in the assets file.")

def analyze_sentiment(text):
    """Analyzes the sentiment of the provided text."""
    analysis = TextBlob(text)
    sentiment = analysis.sentiment.polarity
    if sentiment > 0:
        return "Positive"
    elif sentiment < 0:
        return "Negative"
    else:
        return "Neutral"

def fetch_youtube_comments(api_key, video_id):
    """Fetches comments from a YouTube video."""
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        request = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            maxResults=50
        )
        response = request.execute()

        comments = []
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)

        return comments
    except Exception as e:
        print(f"Error fetching YouTube comments: {e}")
        return []

def analyze_youtube_comments(api_key, video_id):
    """Fetches and analyzes the sentiment of YouTube comments."""
    print("Fetching YouTube comments...")
    comments = fetch_youtube_comments(api_key, video_id)

    if not comments:
        print("No comments found or API limit exceeded.")
        return

    print(f"\nAnalyzing {len(comments)} comments...")
    sentiment_results = {"Positive": 0, "Negative": 0, "Neutral": 0}

    for comment in comments:
        sentiment = analyze_sentiment(comment)
        sentiment_results[sentiment] += 1
        print(f"Comment: {comment}")
        print(f"Sentiment: {sentiment}\n")

    print("\nSummary of Sentiment Analysis:")
    for sentiment, count in sentiment_results.items():
        print(f"{sentiment}: {count}")

def main():
    # File containing asset names
    file_path = "assets.txt"

    # Step 1: Read asset names
    asset_names = read_asset_names(file_path)

    if asset_names:
        # Step 2: Get user input and check for the name
        user_input = input("\nEnter a name to check if it exists in the assets file: ").strip()
        check_name_in_assets(asset_names, user_input)

    # Step 3: Perform sentiment analysis on a static text
    static_text = "YouTube"
    youtube_sentiment = analyze_sentiment(static_text)
    print(f"\nSentiment analysis of '{static_text}': {youtube_sentiment}")

    # Step 4: Analyze sentiment for YouTube comments
    api_key = "" #Replace with Your API key
    video_id = "dQw4w9WgXcQ" 
    analyze_youtube_comments(api_key, video_id)

if __name__ == "__main__":
    main()
