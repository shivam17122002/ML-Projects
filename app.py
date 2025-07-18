import pickle
import streamlit as st
import requests


if 'watchlist' not in st.session_state:
    st.session_state.watchlist = []

st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")

# TMDb API Key
API_KEY = "8265bd1679663a7ea12ac168da84d2e8"

# --- Styling ---
st.markdown("""
    <style>
        .main {
            background-color: #f9f9f9;
        }
        .block-container {
            padding: 2rem 2rem;
        }
        .movie-title {
    font-size: 16px;
    font-weight: 700;
    text-align: center;
    background: linear-gradient(45deg, #00DBDE 0%, #FC00FF 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    text-shadow: 0px 1px 2px rgba(0,0,0,0.1);
    margin-top: 8px;
}

        img {
            border-radius: 15px;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
        }
        .stButton>button {
            background-color: #FF4B4B;
            color: white;
            font-weight: bold;
            border-radius: 10px;
            padding: 0.5rem 1rem;
            transition: 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #ff3a3a;
        }
    </style>
""", unsafe_allow_html=True)

# --- Fetch Functions ---
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    return f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else "https://via.placeholder.com/500x750?text=No+Image"

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_names = []
    recommended_posters = []
    for i in distances[1:7]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_names.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    return recommended_names, recommended_posters

def fetch_trending_movies():
    url = f"https://api.themoviedb.org/3/trending/movie/week?api_key={API_KEY}"
    data = requests.get(url).json()
    trending_names = []
    trending_posters = []
    for movie in data['results'][:6]:
        trending_names.append(movie['title'])
        trending_posters.append(f"https://image.tmdb.org/t/p/w500/{movie['poster_path']}")
    return trending_names, trending_posters

# --- Load Data ---
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# --- Header ---
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>🎬 Movie Recommender System</h1>", unsafe_allow_html=True)
st.markdown("### <center>Find similar movies you’ll love and check out the weekly trending list!</center>", unsafe_allow_html=True)
st.markdown("---")

# --- Movie Input ---
selected_movie = st.selectbox("🎯 Select a Movie", movies['title'].values)

# --- Recommendations ---
if st.button('✨ Show Recommendations'):
    st.markdown("## 📽️ Recommended for You")
    recommended_names, recommended_posters = recommend(selected_movie)
    cols = st.columns(6)
    for i in range(6):
        with cols[i]:
            st.image(recommended_posters[i], use_container_width=True)
            st.markdown(f"<div class='movie-title'>{recommended_names[i]}</div>", unsafe_allow_html=True)
            if st.button(f"➕ Add to Watchlist {i}", key=f"watchlist_button_{i}"):
                movie = {
                    "name": recommended_names[i],
                    "poster": recommended_posters[i]
                }
                if movie not in st.session_state.watchlist:
                    st.session_state.watchlist.append(movie)
                    st.success(f"'{movie['name']}' added to Watchlist")

# --- Divider ---
st.markdown("---")

# --- Trending Movies ---
st.markdown("## 🔥 Top Trending Movies This Week")
trending_names, trending_posters = fetch_trending_movies()
cols = st.columns(6)
for i in range(6):
    with cols[i]:
        st.image(trending_posters[i], use_container_width=True) 
        st.markdown(f"<div class='movie-title'>{trending_names[i]}</div>", unsafe_allow_html=True)

# --- Divider ---
st.markdown("---")

# --- Watchlist Section ---
st.markdown("## 🎯 Your Watchlist")

if st.session_state.watchlist:
    cols = st.columns(6)
    for idx, movie in enumerate(st.session_state.watchlist):
        with cols[idx % 6]:
            st.image(movie['poster'], use_container_width=True)
            st.markdown(f"<div class='movie-title'>{movie['name']}</div>", unsafe_allow_html=True)
else:
    st.info("Your watchlist is empty. Add some movies!")




