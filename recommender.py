import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def build_opportunity_matrix(opportunities_df):
    """
    Build TF-IDF matrix from opportunity descriptions for similarity comparison.
    """
    if 'text' not in opportunities_df.columns:
        opportunities_df['text'] = (
            opportunities_df['title'].fillna('') + " " +
            opportunities_df['description'].fillna('') + " " +
            opportunities_df['skills_required'].fillna('')
        )

    tf = TfidfVectorizer(max_features=2000, stop_words='english')
    X = tf.fit_transform(opportunities_df['text'].values)
    return tf, X

def recommend_for_volunteer(volunteer_profile_text, tf, X, opportunities_df, top_n=5):
    """
    Recommend top N opportunities for a volunteer based on their profile text.
    """
    v_vec = tf.transform([volunteer_profile_text])
    sims = cosine_similarity(v_vec, X).flatten()

    top_idx = np.argsort(-sims)[:min(top_n, len(sims))]
    
    recommended = opportunities_df.iloc[top_idx].copy()
    recommended['score'] = sims[top_idx]
    return recommended.reset_index(drop=True)