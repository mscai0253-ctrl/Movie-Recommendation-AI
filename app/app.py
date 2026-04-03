import sys
import os
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd

from src.auth import *
from src.user_data import *
from src.recommend import *
from src.ai_search import *
from src.poster import *
from src.trailer import *
from src.preprocess_movies import load_movies

# ================= SESSION =================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = ""

# ================= CONFIG =================
st.set_page_config(page_title="Movie Recommender", layout="wide")

# ================= STYLE =================
st.markdown("""
<style>

/* Full width fix */
.main .block-container {
    max-width: 100%;
    padding-left: 2rem;
    padding-right: 2rem;
}

/* Clean UI */
html, body, .stApp {
    background-color: #f8f9fb;
    color: #111;
}

/* Cards */
.card {
    background: white;
    padding: 10px;
    border-radius: 12px;
    border: 1px solid #eee;
    text-align: center;
}

/* Button */
.stButton>button {
    background-color: #111;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# ================= LOAD =================
create_tables()
movies = load_movies()

# ================= TITLE =================
st.title(" Movie Recommendation System")

# ================= SIDEBAR =================
with st.sidebar:
    st.header("Navigation")
    menu = st.radio("", ["Login", "Signup"])
    st.write(f"Movies: {len(movies)}")

# ================= SIGNUP =================
if menu == "Signup":
    st.subheader("Create Account")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Create Account"):
        add_user(u, p)
        st.success("Account created!")

# ================= LOGIN =================
elif menu == "Login":

    if not st.session_state.logged_in:

        st.subheader("Login")

        u = st.text_input("Username")
        p = st.text_input("Password", type="password")

        if st.button("Login"):
            if login_user(u, p):
                st.session_state.logged_in = True
                st.session_state.user = u
                st.rerun()
            else:
                st.error("Invalid credentials")

    if st.session_state.logged_in:

        st.success(f"Welcome {st.session_state.user}")

        # SEARCH
        st.subheader("Search")

        query = st.text_input("Search by genre / mood")

        if query:
            results = search_movies(query)
            for m in results:
                st.write("•", m)

        st.markdown("---")

        # INPUT
        movie = st.selectbox("Select Movie", movies['title'])
        rating = st.slider("Your rating", 1, 5, 3)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Save"):
                save_rating(st.session_state.user, movie, rating)
                st.success("Saved")

        with col2:
            recommend_btn = st.button("Recommend")

        # ================= RECOMMEND =================
        if recommend_btn:

            recs = recommend(movie, get_user_ratings(st.session_state.user))

            # 🔥 FIX 1: RANDOMIZE (new results every click)
            random.shuffle(recs)

            # 🔥 FIX 2: TAKE 20 MOVIES
            recs = recs[:20]

            st.markdown("## 🎯 Recommended Movies")

            # 🔥 FIX 3: CLEAN GRID (NO EMPTY BOXES)
            cols = st.columns(5)

            for i, m in enumerate(recs):
                with cols[i % 5]:

                    st.markdown('<div class="card">', unsafe_allow_html=True)

                    st.markdown(f"**{m}**")

                    poster = movies[movies['title'] == m]['poster_link'].values

                    # 🔥 FIX 4: NO WARNING
                    if len(poster) > 0:
                        st.image(poster[0], width=160)
                    else:
                        st.image(fetch_poster(m), width=160)

                    vid = get_trailer(m)
                    if vid:
                        st.link_button(
                            "▶ Trailer",
                            f"https://www.youtube.com/watch?v={vid}"
                        )

                    st.markdown("</div>", unsafe_allow_html=True)