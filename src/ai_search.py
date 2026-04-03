from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src.preprocess_movies import load_movies  # ✅ correct import

# Load dataset
movies = load_movies()

# Combine title + genres (safe)
movies['combined'] = movies['title'].fillna('') + " " + movies['genres'].fillna('')

# Create vectorizer
vectorizer = TfidfVectorizer(stop_words='english')
vectors = vectorizer.fit_transform(movies['combined'])

def search_movies(query):
    if not query:
        return []

    # Transform query
    q_vec = vectorizer.transform([query])

    # Calculate similarity
    similarity = cosine_similarity(q_vec, vectors).flatten()

    # Get top 5 results
    idx = similarity.argsort()[-5:][::-1]

    return movies.iloc[idx]['title'].tolist()