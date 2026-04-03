from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src.preprocess_movies import load_movies
movies = load_movies()

cv = CountVectorizer(stop_words='english')
vectors = cv.fit_transform(movies['genres'])
similarity = cosine_similarity(vectors)

def recommend(movie, ratings):
    idx = movies[movies['title']==movie].index[0]
    dist = similarity[idx]

    items = sorted(list(enumerate(dist)), key=lambda x:x[1], reverse=True)[1:10]

    result=[]
    for i in items:
        score=i[1]

        for m,r in ratings:
            if r>=4:
                score+=0.1

        result.append((movies.iloc[i[0]].title, score))

    result.sort(key=lambda x:x[1], reverse=True)

    return [i[0] for i in result[:5]]