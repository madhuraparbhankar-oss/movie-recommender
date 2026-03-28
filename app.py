import streamlit as st
import pickle
import requests

st.set_page_config(page_title="Netflix AI", layout="wide")

# 🔥 LOAD DATA FROM GOOGLE DRIVE (FIXED)
@st.cache_data
def load_pickle(file_id):
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    response = requests.get(url)
    return pickle.loads(response.content)

# 👉 PUT YOUR FILE IDs HERE
MOVIES_ID = "YOUR_MOVIES_FILE_ID"
SIMILARITY_ID = "YOUR_SIMILARITY_FILE_ID"

with st.spinner("Loading data... please wait ⏳"):
    movies = load_pickle(MOVIES_ID)
    similarity = load_pickle(SIMILARITY_ID)

# 🎬 Poster (placeholder)
def fetch_poster(movie_title):
    return "https://via.placeholder.com/300x450/000000/FFFFFF?text=" + movie_title.replace(" ", "+")

# 🎯 Recommend function
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]

    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    names, posters = [], []

    for i in movie_list:
        title = movies.iloc[i[0]].title
        names.append(title)
        posters.append(fetch_poster(title))

    return names, posters

# 🎨 CSS
st.markdown("""
<style>
body {
    background: linear-gradient(to bottom, #000000, #141414);
    color: white;
}
.header {
    font-size: 60px;
    color: #E50914;
    text-align: center;
    font-weight: bold;
}
.subtitle {
    text-align: center;
    color: #bbb;
    margin-bottom: 40px;
}
.stButton button {
    background-color: #E50914;
    color: white;
    border-radius: 8px;
    height: 45px;
    width: 200px;
    margin: auto;
    display: block;
}
.card {
    background-color: #181818;
    padding: 10px;
    border-radius: 12px;
    text-align: center;
}
.movie-title {
    font-size: 14px;
    margin-top: 10px;
    color: #fff;
}
</style>
""", unsafe_allow_html=True)

# 🎬 Header
st.markdown("<div class='header'>NETFLIX AI</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Smart Movie Recommendation System</div>", unsafe_allow_html=True)

# 🔍 Select movie
selected_movie = st.selectbox("", movies['title'].values)

# 🎯 Button
if st.button("🍿 Get Recommendations"):
    names, posters = recommend(selected_movie)

    st.markdown("## 🔥 Top Picks For You")

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.image(posters[i])
            st.markdown(f"<div class='movie-title'>{names[i]}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)