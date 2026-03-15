import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

movies = pd.read_csv("movies.csv", low_memory=False)

movies = movies[['title','overview','popularity']]
movies = movies.dropna()

# reduce dataset size to avoid memory issues
movies = movies.sort_values(by="popularity", ascending=False)
movies = movies.head(5000)
movies = movies.reset_index(drop=True)

tfidf = TfidfVectorizer(stop_words="english")
tfidf_matrix = tfidf.fit_transform(movies['overview'])

similarity = cosine_similarity(tfidf_matrix)

def recommend(movie):

    if movie not in movies['title'].values:
        return []

    index = movies[movies['title']==movie].index[0]

    scores = list(enumerate(similarity[index]))

    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    scores = scores[1:7]

    movie_indices = [i[0] for i in scores]

    return movies['title'].iloc[movie_indices].tolist()
