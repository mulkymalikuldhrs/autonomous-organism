from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

# The VADER lexicon is required for sentiment analysis.
# The VADER lexicon is required for sentiment analysis.
# We'll try to find it, and if it's not there, we'll download it.
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    print("Downloading VADER lexicon for sentiment analysis...")
    nltk.download('vader_lexicon')

def analyze_problems(texts: list[str]):
    """
    Analyzes a list of texts to find clusters and sentiment.
    """
    if not texts:
        return {"clusters": [], "sentiment": []}

    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(texts)

    # KMeans Clustering
    # Let's assume we want to find 5 clusters
    num_clusters = min(len(texts), 5)
    kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
    kmeans.fit(X)
    clusters = kmeans.labels_.tolist()

    # Sentiment Analysis
    sia = SentimentIntensityAnalyzer()
    sentiments = [sia.polarity_scores(text) for text in texts]

    # Combine results
    results = []
    for i, text in enumerate(texts):
        results.append({
            "text": text,
            "cluster": clusters[i],
            "sentiment": sentiments[i]
        })

    return results

if __name__ == '__main__':
    # Example usage
    sample_texts = [
        "I hate that my phone battery dies so quickly.",
        "The new software update is buggy and slow.",
        "I wish there was an app to help me find parking.",
        "Customer service was terrible, they never solve the issue.",
        "Finding a good place to eat is always a challenge.",
        "This is the best product I have ever used!",
    ]
    analysis = analyze_problems(sample_texts)
    import json
    print(json.dumps(analysis, indent=2))
