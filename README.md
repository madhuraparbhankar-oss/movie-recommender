This project recommends movies using content-based filtering.
Built with Python, Scikit-learn, and Streamlit.
# Cinematiq AI V2.0 
**A Quantum Movie Recommendation Engine**

This project is an advanced, content-based movie recommendation system that suggests films based on cosine similarity logic. It features a complete futuristic UI overhaul, real-time IMDb data scraping, and is optimized for zero-hassle cloud deployment.

##  Features
* **Machine Learning Core**: Uses Scikit-Learn to calculate Cosine Similarity across thousands of movie tags to find the absolute best matches.
* **Cyberpunk Glassmorphism UI**: Built with Streamlit but heavily customized with raw CSS for neon gradients, glowing shadows, hover animations, and futuristic web-fonts (`Orbitron` & `Rajdhani`).
* **Zero-Auth IMDb Integration**: Automatically searches IMDb's hidden autocomplete endpoints in the background to fetch high-res movie posters, release years, and cast members—all without requiring any API keys.
* **Dynamic Hyperlinks**: Click "Access Data" on any recommended movie to instantly open its official IMDb page.
* **Large File Handling**: Built natively to bypass GitHub's 100MB file limit by silently downloading the massive 200MB similarity matrix directly from Google Drive into RAM during startup.

##  How It Works
1. **Data Initialization**: When the app starts, it checks if `movies.pkl` and `similarity.pkl` exist locally. If they don't (like on a fresh Streamlit Cloud deployment), it securely downloads them using `gdown`.
2. **Matrix Lookup**: When you select a target movie, the system looks up its vector index in the pre-computed similarity matrix.
3. **Sorting**: It sorts the numerical distances to find the top mathematically closest movies.
4. **Data Scraping**: The app parses the titles, encodes them into URL-safe strings, and pings IMDb's suggestion API to grab the poster and metadata.
5. **Rendering**: The Streamlit interface generates custom HTML/CSS cards for each result and displays them in a dynamic grid.

##  Running Locally
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the Streamlit application
streamlit run app.py
```

##  Deployment
This repository is pre-configured for **Streamlit Community Cloud**. 
Because it uses `gdown` inside `@st.cache_resource`, it will effortlessly bypass GitHub's LFS limits and download the required dataset automatically during the cloud build process. Just deploy the `main` branch to share.streamlit.io!
