import streamlit as st
import pickle
import re
import nltk
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('stopwords', quiet=True)
stop_words = set(stopwords.words('english'))

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    words = text.split()
    words = [w for w in words if w not in stop_words]
    return " ".join(words)

with open("model.pkl", "rb") as f:
    vectorizer, tfidf_matrix, df = pickle.load(f)

st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")

st.title("🎬 IMDB 2024 Movie Recommendation System")
st.markdown("Enter a movie storyline below and get **Top 5 similar movies**!")

user_input = st.text_area("📝 Enter a Storyline:", height=150, 
    placeholder="Example: A soldier fights behind enemy lines during World War II...")

if st.button("🔍 Recommend Movies"):
    if user_input.strip() == "":
        st.warning("Please enter a storyline!")
    else:
        cleaned = clean_text(user_input)
        input_vec = vectorizer.transform([cleaned])
        sim_scores = cosine_similarity(input_vec, tfidf_matrix).flatten()
        top_indices = sim_scores.argsort()[::-1][:5]
        
        st.subheader("🎯 Top 5 Recommended Movies:")
        for rank, idx in enumerate(top_indices, 1):
            score = round(sim_scores[idx] * 100, 2)
            st.markdown(f"### {rank}. {df.iloc[idx]['Movie Name']}")
            st.write(f"**Storyline:** {df.iloc[idx]['Storyline']}")
            st.progress(score / 100)
            st.caption(f"Similarity Score: {score}%")
            st.divider()