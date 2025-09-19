import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def build_opportunity_matrix(opportunities_df):
    tf = TfidfVectorizer(max_features=2000, stop_words='english')
    X = tf.fit_transform(opportunities_df['text'].values)
    return tf, X

def recommend_for_volunteer(volunteer_profile_text, tf, X, opportunies_df, top_n=5):
    v_vec = tf.transform([volunteer_profile_text])
    sims = cosine_similarity(v_vec, X).flatten()
    top_idx = np.argsort(-sims)[:top_n]
    return opportunies_df.iloc[top_idx].copy().assign(score=sims[top_idx])