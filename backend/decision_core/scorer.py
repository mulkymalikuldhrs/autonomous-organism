import pandas as pd

def score_clusters(df: pd.DataFrame):
    """
    Scores clusters based on the formula provided in the blueprint.

    Args:
        df: A pandas DataFrame with columns for cluster, sentiment scores, etc.

    Returns:
        A pandas DataFrame with the scores for each cluster.
    """
    if df.empty:
        return pd.DataFrame(columns=['cluster', 'score', 'complaint_count', 'negative_emotion', 'summary'])

    # These are placeholders for now
    automation_potential = 0.8 # Assume a high potential for now
    money_potential = 0.5 # Assume a medium potential for now

    cluster_scores = []
    for cluster_num in df['cluster'].unique():
        cluster_df = df[df['cluster'] == cluster_num]

        complaint_count = len(cluster_df)
        negative_emotion = cluster_df['neg'].mean()

        score = (
            (complaint_count * 0.4) +
            (negative_emotion * 0.2) +
            (automation_potential * 0.2) +
            (money_potential * 0.2)
        )

        # Simple summary for now
        summary = cluster_df['problem'].iloc[0]

        cluster_scores.append({
            'cluster': cluster_num,
            'score': score,
            'complaint_count': complaint_count,
            'negative_emotion': negative_emotion,
            'summary': summary
        })

    scored_df = pd.DataFrame(cluster_scores)
    return scored_df.sort_values(by='score', ascending=False)
