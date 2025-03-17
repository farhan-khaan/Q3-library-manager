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

# Custom CSS for enhanced UI
st.markdown("""
    <style>
        /* Main title styling */
        .main-header {
            font-size: 3rem !important;
            color: #1E3A8A;
            font-weight: 700;
            margin-bottom: 1rem;
            text-align: center;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }

        /* Subheader styling */
        .sub-header {
            font-size: 1.8rem !important;
            color: #3B82F6;
            font-weight: 600;
            margin-top: 1rem;
            margin-bottom: 1rem;
        }

        /* Book card styling */
        .book-card {
            background-color: #F3F4F6;
            border-radius: 0.5rem;
            padding: 1rem;
            margin-bottom: 1rem;
            border-left: 5px solid #3B82F6;
            transition: transform 0.3s ease;
        }
        .book-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        }

        /* Read/Unread badges */
        .read-badge {
            background-color: #10B981;
            color: white;
            padding: 0.25rem 0.75rem;
            border-radius: 1rem;
            font-size: 0.875rem;
            font-weight: 600;
        }
        .unread-badge {
            background-color: #F87171;
            color: white;
            padding: 0.25rem 0.75rem;
            border-radius: 1rem;
            font-size: 0.875rem;
            font-weight: 600;
        }

        /* Success and Warning Messages */
        .success-message {
            padding: 1rem;
            background-color: #ECFDF5;
            border-left: 5px solid #10B981;
            border-radius: 0.375rem;
        }
        .warning-message {
            padding: 1rem;
            background-color: #FEF3C7;
            border-left: 5px solid #F59E0B;
            border-radius: 0.375rem;
        }

        /* Exit button styling */
        .stButton>button {
            background-color: #E11D48;
            color: white;
            border-radius: 0.375rem;
            font-weight: bold;
            padding: 10px;
            width: 100%;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #BE123C;
        }
    </style>
""", unsafe_allow_html=True)

# Function to exit the library system
def exit_library():
    st.session_state.clear()  # Clears all session data
    st.markdown("<div class='success-message'>✅ Library system closed. You may close the tab.</div>", unsafe_allow_html=True)
    st.stop()  # Stops execution

# Sidebar navigation
st.sidebar.markdown("<h1 class='sub-header'>📖 Library Manager</h1>", unsafe_allow_html=True)

if st.sidebar.button("❌ Exit Library System", use_container_width=True):
    exit_library()

nav_options = st.sidebar.radio("Navigation", ["View Library", "Add Book", "Search Books", "Library Statistics"])
st.session_state.current_view = nav_options.lower().replace(" ", "_")

st.markdown("<h1 class='main-header'>📖 Personal Library Manager</h1>", unsafe_allow_html=True)

# ADD BOOK PAGE
if st.session_state.current_view == "add_book":
    st.markdown("<h2 class='sub-header'>➕ Add a New Book</h2>", unsafe_allow_html=True)
    with st.form(key="add_book_form"):
        title = st.text_input("Book Title")
        author = st.text_input("Author")
        publication_year = st.number_input("Publication Year", min_value=1000, max_value=datetime.now().year, step=1)
        genre = st.selectbox("Genre", ["Fiction", "Non-Fiction", "Science", "Technology", "Fantasy", "Romance", "History", "Other"])
        read_status = st.radio("Read Status", ["Read", "Unread"])
        submit_button = st.form_submit_button("Add Book")

        if submit_button and title and author:
            st.session_state.library.append({
                "title": title,
                "author": author,
                "publication_year": publication_year,
                "genre": genre,
                "read_status": read_status == "Read",
                "added_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            st.markdown("<div class='success-message'>✅ Book added successfully!</div>", unsafe_allow_html=True)

# VIEW LIBRARY PAGE
elif st.session_state.current_view == "view_library":
    st.markdown("<h2 class='sub-header'>📖 Your Library</h2>", unsafe_allow_html=True)
    if not st.session_state.library:
        st.markdown("<div class='warning-message'>⚠️ Your library is empty! Add books to get started.</div>", unsafe_allow_html=True)
    else:
        for book in st.session_state.library:
            st.markdown(f"""
                <div class='book-card'>
                    <h3>{book['title']}</h3>
                    <p><strong>Author:</strong> {book['author']}</p>
                    <p><strong>Year:</strong> {book['publication_year']}</p>
                    <p><strong>Genre:</strong> {book['genre']}</p>
                    <p><span class='{"read-badge" if book["read_status"] else "unread-badge"}'>
                    {"✅ Read" if book["read_status"] else "📖 Unread"}
                    </span></p>
                </div>
            """, unsafe_allow_html=True)

# SEARCH BOOKS PAGE
elif st.session_state.current_view == "search_books":
    st.markdown("<h2 class='sub-header'>🔍 Search Books</h2>", unsafe_allow_html=True)
    search_by = st.selectbox("Search by:", ["Title", "Author", "Genre"])
    search_term = st.text_input("Enter search term:")
    if st.button("Search"):
        results = [book for book in st.session_state.library if search_term.lower() in book[search_by.lower()].lower()]
        if results:
            for book in results:
                st.markdown(f"📘 **{book['title']}** by {book['author']} ({book['publication_year']})")
        else:
            st.markdown("<div class='warning-message'>⚠️ No books found matching your search.</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("© 2025 Personal Library Manager by Farhan Khan")
