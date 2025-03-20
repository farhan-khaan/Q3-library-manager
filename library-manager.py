import streamlit as st
import pandas as pd
import json
import os
import time
import requests
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from streamlit_lottie import st_lottie

# Set Streamlit page config
st.set_page_config(page_title="Personal Library Manager", page_icon="📖", layout="wide")

# Function to load Lottie animation with caching
@st.cache_data
def load_lottieurl(url):
    """Loads a Lottie animation from a URL with caching."""
    try:
        response = requests.get(url, timeout=3)  # Reduced timeout for faster loading
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None  # Prevents app crash if animation fails

# Load Lottie animation
lottie_book = load_lottieurl("https://lottie.host/embed/0c086a61-5972-4466-a993-8bc269ff2466/xAYCI2YK52.lottie")

# Function to load library data
@st.cache_data
def load_library():
    if os.path.exists("library.json"):
        with open("library.json", "r") as file:
            return json.load(file)
    return []

# Function to save library data
def save_library():
    try:
        with open("library.json", "w") as file:
            json.dump(st.session_state.library, file, indent=4)
    except Exception as e:
        st.error(f"Error saving library: {e}")

# Initialize session state variables
if "library" not in st.session_state:
    st.session_state.library = []
if "current_view" not in st.session_state:
    st.session_state.current_view = "library"

# Function to add a book
def add_book(title, author, publication_year, genre, read_status):
    book = {
        "title": title,
        "author": author,
        "publication_year": publication_year,
        "genre": genre,
        "read_status": read_status,
        "added_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    st.session_state.library.append(book)
    save_library()
    st.success("✅ Book added successfully!")
    time.sleep(0.5)
    st.rerun()

# Function to remove a book
def remove_book(index):
    if 0 <= index < len(st.session_state.library):
        del st.session_state.library[index]
        save_library()
        st.success("❌ Book removed successfully!")
        st.rerun()

# Function to search books
def search_books(search_term, search_by):
    search_term = search_term.lower()
    st.session_state.search_results = [
        book for book in st.session_state.library if search_term in book[search_by.lower()].lower()
    ]

# Function to get library statistics
def get_library_stats():
    total_books = len(st.session_state.library)
    read_books = sum(1 for book in st.session_state.library if book["read_status"])
    percent_read = (read_books / total_books * 100) if total_books > 0 else 0

    genres = {}
    authors = {}
    decades = {}

    for book in st.session_state.library:
        genres[book["genre"]] = genres.get(book["genre"], 0) + 1
        authors[book["author"]] = authors.get(book["author"], 0) + 1
        decade = (book["publication_year"] // 10) * 10
        decades[decade] = decades.get(decade, 0) + 1

    return {"total_books": total_books, "read_books": read_books, "percent_read": percent_read, "genres": genres, "authors": authors, "decades": decades}

# Sidebar navigation
st.sidebar.title("📖 Library Manager")

# Display animation in sidebar if successfully loaded
if lottie_book:
    with st.sidebar:
        st_lottie(lottie_book, height=200, key="book_animation")

nav_options = st.sidebar.radio("Navigation", ["View Library", "Add Book", "Search Books", "Library Statistics"])
st.session_state.current_view = nav_options.lower().replace(" ", "_")

st.title("📖 Personal Library Manager")

# ADD BOOK PAGE
if st.session_state.current_view == "add_book":
    st.subheader("➕ Add a New Book")
    with st.form(key="add_book_form"):
        title = st.text_input("Book Title")
        author = st.text_input("Author")
        publication_year = st.number_input("Publication Year", min_value=1000, max_value=datetime.now().year, step=1)
        genre = st.selectbox("Genre", ["Fiction", "Non-Fiction", "Science", "Technology", "Fantasy", "Romance", "History", "Other"])
        read_status = st.radio("Read Status", ["Read", "Unread"])
        submit_button = st.form_submit_button("Add Book")

        if submit_button and title and author:
            add_book(title, author, publication_year, genre, read_status == "Read")

# VIEW LIBRARY PAGE
elif st.session_state.current_view == "view_library":
    st.subheader("📖 Your Library")
    if not st.session_state.library:
        st.warning("Your library is empty! Add some books to get started.")
    else:
        for i, book in enumerate(st.session_state.library):
            with st.expander(f"📘 {book['title']} by {book['author']} ({book['publication_year']})"):
                st.write(f"**Genre:** {book['genre']}")
                st.write(f"**Status:** {'✅ Read' if book['read_status'] else '📖 Unread'}")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("❌ Remove", key=f"remove_{i}"):
                        remove_book(i)
                with col2:
                    new_status = not book["read_status"]
                    if st.button("✅ Mark as Read" if not new_status else "📖 Mark as Unread", key=f"status_{i}"):
                        st.session_state.library[i]["read_status"] = new_status
                        save_library()
                        st.rerun()

# SEARCH BOOKS PAGE
elif st.session_state.current_view == "search_books":
    st.subheader("🔍 Search Books")
    search_by = st.selectbox("Search by:", ["Title", "Author", "Genre"])
    search_term = st.text_input("Enter search term:")
    if st.button("Search"):
        search_books(search_term, search_by)
    if "search_results" in st.session_state and st.session_state.search_results:
        for book in st.session_state.search_results:
            st.write(f"📘 **{book['title']}** by {book['author']} ({book['publication_year']})")

# LIBRARY STATISTICS PAGE
elif st.session_state.current_view == "library_statistics":
    st.subheader("📊 Library Statistics")
    stats = get_library_stats()
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Books", stats["total_books"])
    col2.metric("Books Read", stats["read_books"])
    col3.metric("Percentage Read", f"{stats['percent_read']:.1f}%")

st.markdown("---")
st.caption("© 2025 Personal Library Manager by Farhan Khan")
