import streamlit as st
import pickle
import os
import gdown

st.set_page_config(page_title="Netflix AI", layout="wide")

# 🔥 LOAD DATA (Google Drive FIXED)
@st.cache_resource
def load_pickle(file_path, file_id):
    if not os.path.exists(file_path) or os.path.getsize(file_path) < 10000:
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(url, file_path, quiet=False)

    with open(file_path, "rb") as f:
        return pickle.load(f)

# 👉 YOUR FILE IDs
MOVIES_ID = "14fBRVtQNF_RVWQ3eBX4_8TXh_W1cL61M"
SIMILARITY_ID = "17q9sI0nyvAfABzUCJPhWxeuYrJaEwTsW"

# ⏳ Load Data
with st.spinner("Loading data... ⏳"):
    movies = load_pickle("movies.pkl", MOVIES_ID)
    similarity = load_pickle("similarity.pkl", SIMILARITY_ID)

# 🎬 Placeholder Posters (NO API)
def fetch_poster(movie_title):
    return f"https://placehold.co/300x450/1c1c1c/FFF?text={movie_title.replace(' ', '+')}"

# 🎯 Recommendation Function
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    names, posters = [], []

    for i in movie_list:
        title = movies.iloc[i[0]].title
        names.append(title)
        posters.append(fetch_poster(title))

    return names, posters

# 🎨 CLEAN DARK UI
st.markdown("""
<style>
body {
    background-color: #0e1117;
}

.header {
    font-size: 50px;
    color: #E50914;
    text-align: center;
    font-weight: bold;
}

.subtitle {
    text-align: center;
    color: #aaa;
    margin-bottom: 30px;
}

.movie-card {
    background-color: #1c1c1c;
    padding: 10px;
    border-radius: 15px;
    text-align: center;
    transition: 0.3s;
}

.movie-card:hover {
    transform: scale(1.05);
}

.movie-title {
    font-size: 14px;
    margin-top: 10px;
    color: white;
}

.stButton>button {
    background-color: #E50914;
    color: white;
    border-radius: 10px;
    height: 45px;
    width: 250px;
    display: block;
    margin: auto;
}
</style>
""", unsafe_allow_html=True)

# 🎬 HEADER
st.markdown("<div class='header'>🎬 Movie Recommender</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Find movies you'll love instantly</div>", unsafe_allow_html=True)

# 🔍 CENTERED SEARCH
col1, col2, col3 = st.columns([1,2,1])

with col2:
    selected_movie = st.selectbox("Search Movie", movies['title'].values)

# 🎯 BUTTON CENTER
col_btn1, col_btn2, col_btn3 = st.columns([1,1,1])

with col_btn2:
    clicked = st.button("🍿 Get Recommendations")

# 🎬 RESULTS
if clicked:
    names, posters = recommend(selected_movie)

    st.markdown("## 🔥 Top Picks For You")

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            card_html = f"""
            <div class='movie-card'>
                <img src="{posters[i]}" style="width:100%; border-radius:10px; margin-bottom:10px;">
                <div class='movie-title'>{names[i]}</div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)