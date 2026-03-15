import streamlit as st
import requests
from recommender import recommend, movies

TMDB_API_KEY = "20ad6fa2427d097a807f4bc53fc6531c"

st.title("🎬 Movie Recommendation System")


# -----------------------------
# Clean movie title
# -----------------------------
def clean_title(movie):
    return movie.split("(")[0].strip()


# -----------------------------
# Get movie details from TMDb
# -----------------------------
@st.cache_data
def get_movie_details(movie):

    movie = clean_title(movie)

    try:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie}"

        data = requests.get(url, timeout=10).json()

        if data.get("results"):

            movie_data = data["results"][0]

            poster = None
            if movie_data.get("poster_path"):
                poster = "https://image.tmdb.org/t/p/w500" + movie_data["poster_path"]

            overview = movie_data.get("overview")

            movie_id = movie_data.get("id")

            return poster, overview, movie_id

    except:
        return None, None, None

    return None, None, None


# -----------------------------
# Get trailer
# -----------------------------
@st.cache_data
def get_trailer(movie_id):

    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={TMDB_API_KEY}"

        data = requests.get(url, timeout=10).json()

        for video in data.get("results", []):

            if video["type"] == "Trailer":

                return f"https://www.youtube.com/watch?v={video['key']}"

    except:
        return None

    return None


# -----------------------------
# Manual Trending Movies
# -----------------------------
st.subheader("🔥 Trending Movies")

trending_movies = [
    "Oppenheimer",
    "Barbie",
    "Dhurandhar",
    "Avatar",
    "Interstellar",
    "Jawan",
    "RRR",
    "Dangal"
]

for movie in trending_movies:

    poster, overview, movie_id = get_movie_details(movie)

    trailer = None
    if movie_id:
        trailer = get_trailer(movie_id)

    col1, col2 = st.columns([1,2])

    with col1:
        if poster:
            st.image(poster)

    with col2:
        st.subheader(movie)

        if overview:
            st.write(overview)

        if trailer:
            st.link_button("▶ Watch Trailer", trailer)


# -----------------------------
# Recommendation Section
# -----------------------------
st.subheader("🎥 Movie Recommendations")

movie_list = movies['title'].dropna().unique()

selected_movie = st.selectbox(
    "Select a movie",
    movie_list
)

if st.button("Recommend"):

    recommendations = recommend(selected_movie)

    cols = st.columns(3)

    for i, movie in enumerate(recommendations):

        poster, overview, movie_id = get_movie_details(movie)

        with cols[i % 3]:

            if poster:
                st.image(poster)

            st.caption(movie)