import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import time
import plotly.express as px
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import requests
import sys

# Set page configuration
st.set_page_config(
    page_title="Personal Library Manager",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state if not set
if "library" not in st.session_state:
    st.session_state.library = []
    
if "book_added" not in st.session_state:
    st.session_state.book_added = False

# Load Lottie animation function
def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Sidebar navigation
st.sidebar.markdown("<h1 style='text-align: center;'>📖 Navigation</h1>", unsafe_allow_html=True)

# Display Lottie animation in sidebar
lottie_book = load_lottieurl("https://lottie.host/embed/0c086a61-5972-4466-a993-8bc269ff2466/xAYCI2YK52.lottie")
if lottie_book:
    with st.sidebar:
        st_lottie(lottie_book, height=200, key="book_animation")

# Navigation options
nav_options = st.sidebar.radio(
    "📌 Choose an option:",
    ["📚 View Library", "➕ Add Book", "🔍 Search Books", "📊 Library Statistics"]
)

# Exit button
if st.sidebar.button("🚪 Exit App"):
    st.warning("Closing the application...")
    time.sleep(1)
    sys.exit()

# Page Title
st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>📚 Personal Library Manager</h1>", unsafe_allow_html=True)

# Handle navigation
if nav_options == "📚 View Library":
    st.subheader("📖 Your Library")
    if st.session_state.library:
        for book in st.session_state.library:
            st.markdown(f"**Title:** {book['title']}")
            st.markdown(f"**Author:** {book['author']}")
            st.markdown(f"**Genre:** {book['genre']}")
            st.markdown(f"**Publication Year:** {book['publication_year']}")
            st.markdown(f"**Read Status:** {'Read' if book['read'] else 'Unread'}")
            if book.get('image'):
                st.image(book['image'], width=150)
            if book.get('pdf'):
                st.markdown(f"[📄 Download PDF]({book['pdf']})")
            st.markdown("---")
    else:
        st.write("No books in the library yet.")

elif nav_options == "➕ Add Book":
    st.subheader("➕ Add a New Book")
    with st.form(key='add_book_form'):
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("Book Title", max_chars=100)
            author = st.text_input("Author", max_chars=100)
            publication_year = st.number_input("Publication Year", min_value=1000, max_value=datetime.now().year, step=1, value=2023)
        
        with col2:
            genre = st.selectbox("Genre", [
                "Fiction", "Non-Fiction", "Science", "Technology", "Fantasy", "Romance", "Poetry", "Self-help", "Art", "Religion", "History", "Other"
            ])
            read_status = st.radio("Read Status", ["Read", "Unread"], horizontal=True)
            read_bool = read_status == "Read"
        
        image = st.file_uploader("Upload Book Cover (Optional)", type=["png", "jpg", "jpeg"])
        pdf = st.file_uploader("Upload Book PDF (Optional)", type=["pdf"])
        
        submit_button = st.form_submit_button(label="Add Book")

        if submit_button and title and author:
            book_data = {
                "title": title,
                "author": author,
                "publication_year": publication_year,
                "genre": genre,
                "read": read_bool,
                "image": None,
                "pdf": None
            }
            if image is not None:
                book_data["image"] = image
            if pdf is not None:
                book_data["pdf"] = pdf
            
            st.session_state.library.append(book_data)
            st.session_state.book_added = True
            st.success("Book added successfully!")
            st.balloons()

    if st.session_state.book_added:
        st.markdown("<div class='success-message'>Book added successfully!</div>", unsafe_allow_html=True)
        st.session_state.book_added = False

elif nav_options == "🔍 Search Books":
    st.subheader("🔍 Search Books")
    st.write("Search functionality...")

elif nav_options == "📊 Library Statistics":
    st.subheader("📊 Library Statistics")
    st.write("Statistics visualization...")

st.markdown("---")
st.markdown("© 2025, Library Management by Farhan Khan", unsafe_allow_html=True)
