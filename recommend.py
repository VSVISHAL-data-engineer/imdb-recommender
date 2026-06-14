import pandas as pd
import re
import nltk
import pickle
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('stopwords')

df = pd.read_csv("imdb_2024_movies.csv")
df = df.dropna(subset=["Storyline"])
df = df[df["Storyline"].str.strip() != ""].reset_index(drop=True)

stop_words = set(stopwords.words('english'))

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    words = text.split()
    words = [w for w in words if w not in stop_words]
    return " ".join(words)

df["clean_storyline"] = df["Storyline"].apply(clean_text)

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df["clean_storyline"])

with open("model.pkl", "wb") as f:
    pickle.dump((vectorizer, tfidf_matrix, df), f)

print("Model saved successfully!")
print(f"Total movies in model: {len(df)}")