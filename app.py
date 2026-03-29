import streamlit as st
import pickle
import os
import gdown
import requests
import urllib.parse

st.set_page_config(page_title="Cinematiq AI", layout="wide", page_icon="🌌")

# 🔥 LOAD DATA
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
with st.spinner("Initializing Neural Network... 🌌"):
    movies = load_pickle("movies.pkl", MOVIES_ID)
    similarity = load_pickle("similarity.pkl", SIMILARITY_ID)

# 🎬 Movie Details Fetching (IMDB API)
@st.cache_data
def fetch_movie_details(movie_title):
    try:
        clean_title = urllib.parse.quote(movie_title.lower())
        first_letter = clean_title[0] if clean_title else 'a'
        url = f"https://v2.sg.media-imdb.com/suggestion/{first_letter}/{clean_title}.json"
        
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=5)
        data = response.json()
        
        if "d" in data and len(data["d"]) > 0:
            movie_data = data["d"][0]
            poster_url = movie_data.get("i", {}).get("imageUrl")
            year = movie_data.get("y", "Unknown")
            cast = movie_data.get("s", "Unknown Cast")
            imdb_id = movie_data.get("id", "")
            
            if poster_url:
                return poster_url, year, cast, imdb_id
    except Exception as e:
        pass
        
    fallback = f"https://placehold.co/300x450/1c1c1c/FFF?text={movie_title.replace(' ', '+')}"
    return fallback, "Unknown", "Unknown", ""

# 🎯 Recommendation Function
def recommend(movie, top_n=5):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:top_n+1]

    recommendations = []
    
    for i in movie_list:
        title = movies.iloc[i[0]].title
        poster, year, cast, imdb_id = fetch_movie_details(title)
        recommendations.append({
            "title": title,
            "poster": poster,
            "year": year,
            "cast": cast,
            "imdb_id": imdb_id
        })

    return recommendations

# 🎨 FUTURISTIC CYBERPUNK UI
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@400;600&display=swap');

body, .stApp {
    background: #050505;
    background-image: radial-gradient(circle at 50% 0%, #1a0b2e 0%, #050505 60%);
    color: #e0e0e0;
    font-family: 'Rajdhani', sans-serif;
}

.header {
    font-size: 65px;
    font-family: 'Orbitron', sans-serif;
    background: -webkit-linear-gradient(45deg, #00f2fe, #4facfe, #f093fb, #f5576c);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    font-weight: bold;
    text-shadow: 0px 0px 20px rgba(79, 172, 254, 0.5);
    margin-bottom: 0px;
    padding-bottom: 10px;
}

.subtitle {
    text-align: center;
    color: #4facfe;
    font-size: 22px;
    font-family: 'Orbitron', sans-serif;
    letter-spacing: 3px;
    margin-bottom: 40px;
    text-transform: uppercase;
}

/* Glassmorphism Cards with Neon Glow */
.movie-card {
    background: rgba(15, 15, 20, 0.6);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 8px 32px 0 rgba(79, 172, 254, 0.15);
    padding: 15px;
    border-radius: 16px;
    text-align: center;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    height: 100%;
    margin-bottom: 20px;
}

.movie-card:hover {
    transform: translateY(-8px) scale(1.02);
    box-shadow: 0 15px 40px 0 rgba(240, 147, 251, 0.4);
    border: 1px solid rgba(240, 147, 251, 0.5);
}

.movie-poster {
    width: 100%;
    border-radius: 12px;
    margin-bottom: 15px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.5);
}

.movie-title {
    font-size: 18px;
    font-family: 'Orbitron', sans-serif;
    color: #ffffff;
    font-weight: bold;
    margin-bottom: 5px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.movie-meta {
    font-size: 16px;
    font-weight: bold;
    color: #4facfe;
    margin-bottom: 5px;
}

.movie-cast {
    font-size: 13px;
    color: #aaaaaa;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    margin-bottom: 15px;
    height: 35px;
}

.imdb-link {
    display: inline-block;
    padding: 6px 15px;
    background: linear-gradient(90deg, #4facfe, #00f2fe);
    color: #000 !important;
    text-decoration: none;
    border-radius: 20px;
    font-weight: bold;
    font-size: 12px;
    font-family: 'Orbitron', sans-serif;
    transition: 0.3s;
}

.imdb-link:hover {
    box-shadow: 0 0 15px rgba(79, 172, 254, 0.8);
    transform: scale(1.05);
}

/* Futuristic Target Button */
.stButton>button {
    background: transparent;
    color: #fff;
    border: 2px solid #f093fb;
    border-radius: 10px;
    height: 48px;
    width: 100%;
    font-size: 16px;
    font-family: 'Orbitron', sans-serif;
    letter-spacing: 2px;
    text-transform: uppercase;
    transition: 0.4s;
    box-shadow: 0 0 10px rgba(240, 147, 251, 0.4) inset;
    margin-top: 25px;
}

.stButton>button:hover {
    background: #f093fb;
    color: #000;
    box-shadow: 0 0 20px rgba(240, 147, 251, 0.8);
}
</style>
""", unsafe_allow_html=True)

# 🌌 SIDEBAR
with st.sidebar:
    st.markdown("<h2 style='font-family: Orbitron; color: #4facfe;'>SYSTEM SETTINGS</h2>", unsafe_allow_html=True)
    num_recommendations = st.slider("Target Matches", min_value=3, max_value=10, value=5)
    st.markdown("---")
    st.markdown("Powered by Neural Cosine Similarity Vectors. Built for the future of cinema. 🍿")

# 🎬 HEADER
st.markdown("<div class='header'>CINEMATIQ AI</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>V2.0 Quantum Engine</div>", unsafe_allow_html=True)

# 🔍 CENTERED SEARCH
col1, col2, col3 = st.columns([1,3,1])

with col2:
    selected_movie = st.selectbox("INITIALIZE TARGET MODULE", movies['title'].values)
    clicked = st.button("🚀 INITIATE SCAN")

# 🎬 RESULTS
if clicked:
    st.markdown("<hr style='border: 1px solid rgba(79, 172, 254, 0.3); margin: 30px 0;'>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; font-family: Orbitron; color: white; text-shadow: 0 0 10px #f093fb;'>🔥 OPTIMAL SYSTEM MATCHES</h2>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    recommendations = recommend(selected_movie, top_n=num_recommendations)

    # Convert to rows of 5 if num_recommendations is large
    # Streamlit columns are best kept at max 5.
    for row in range(0, num_recommendations, 5):
        chunk = recommendations[row:row+5]
        cols = st.columns(len(chunk))
        
        for i, rec in enumerate(chunk):
            with cols[i]:
                imdb_url = f"https://www.imdb.com/title/{rec['imdb_id']}/" if rec['imdb_id'] else "#"
                button_html = f"<div style='margin-top:auto;'><a href='{imdb_url}' target='_blank' class='imdb-link'>ACCESS DATA</a></div>" if rec['imdb_id'] else ""
                
                card_html = f"""
                <div class='movie-card'>
                    <img src="{rec['poster']}" class='movie-poster'>
                    <div class='movie-title' title="{rec['title']}">{rec['title']}</div>
                    <div class='movie-meta'>{rec['year']}</div>
                    <div class='movie-cast'>{rec['cast']}</div>
                    {button_html}
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)
        st.write("") # Spacer between rows