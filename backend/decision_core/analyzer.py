from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import nltk

# Download necessary NLTK data
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader')

def analyze_problems(problems: list[str]):
    """
    Analyzes a list of problems to cluster them and calculate sentiment.

    Args:
        problems: A list of cleaned problem texts.

    Returns:
        A pandas DataFrame with columns for the problem text, cluster, and sentiment scores.
    """
    if not problems:
        return pd.DataFrame(columns=['problem', 'cluster', 'neg', 'neu', 'pos', 'compound'])

    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(problems)

    # KMeans Clustering
    num_clusters = min(5, len(problems)) # Example: 5 clusters or less if fewer problems
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    kmeans.fit(X)
    clusters = kmeans.labels_

    # Sentiment Analysis
    sid = SentimentIntensityAnalyzer()
    sentiments = [sid.polarity_scores(problem) for problem in problems]

    # Create DataFrame
    df = pd.DataFrame({
        'problem': problems,
        'cluster': clusters,
        'neg': [s['neg'] for s in sentiments],
        'neu': [s['neu'] for s in sentiments],
        'pos': [s['pos'] for s in sentiments],
        'compound': [s['compound'] for s in sentiments]
    })

    return df
