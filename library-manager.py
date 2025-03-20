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
            if book.get('image'):
                st.image(book['image'], width=150)
            if book.get('pdf'):
                st.markdown(f"[📄 Download PDF]({book['pdf']})")
            st.markdown("---")
    else:
        st.write("No books in the library yet.")

elif nav_options == "➕ Add Book":
    st.subheader("➕ Add a New Book")
    title = st.text_input("Book Title")
    author = st.text_input("Author")
    image = st.file_uploader("Upload Book Cover (Optional)", type=["png", "jpg", "jpeg"])
    pdf = st.file_uploader("Upload Book PDF (Optional)", type=["pdf"])
    
    if st.button("Add Book"):
        if title and author:
            book_data = {"title": title, "author": author, "image": None, "pdf": None}
            if image is not None:
                book_data["image"] = image
            if pdf is not None:
                book_data["pdf"] = pdf
            st.session_state.library.append(book_data)
            st.success("Book added successfully!")
        else:
            st.error("Please provide both title and author.")

elif nav_options == "🔍 Search Books":
    st.subheader("🔍 Search Books")
    st.write("Search functionality...")

elif nav_options == "📊 Library Statistics":
    st.subheader("📊 Library Statistics")
    st.write("Statistics visualization...")

st.markdown("---")
st.markdown("© 2025, Library Management by Farhan Khan", unsafe_allow_html=True)
