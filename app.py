import sqlite3
import pandas as pd
import streamlit as st
from datetime import date

# Connect to SQLite
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

st.set_page_config(page_title="BookBase", layout="wide")
st.title("📚 BookBase – Library Dashboard")

# Sidebar Navigation 
menu = st.sidebar.radio("Navigate", ["Books", "Members", "Borrowing Records", "Top Borrowed", "Unreturned Books"])

# View: Books
if menu == "Books":
    st.header("📖 Available Books")
    books = pd.read_sql("SELECT * FROM silver_books", conn)
    st.dataframe(books)

# View: Members 
elif menu == "Members":
    st.header("👤 Library Members")
    members = pd.read_sql("SELECT * FROM Members", conn)
    st.dataframe(members)

# View: Borrowing Records 
elif menu == "Borrowing Records":
    st.header("📄 Borrowing Records")
    records = pd.read_sql("SELECT * FROM BorrowingRecords", conn)
    st.dataframe(records)

# View: Top Borrowed Books
elif menu == "Top Borrowed":
    st.header("🏆 Top 10 Most Borrowed Books")
    top_books = pd.read_sql("SELECT * FROM gold_top_borrowed_books", conn)
    st.dataframe(top_books)

    st.header("🏅 Top 10 Members by Borrowing")
    top_members = pd.read_sql("SELECT * FROM gold_top_members", conn)
    st.dataframe(top_members)

# View: Unreturned Books 
elif menu == "Unreturned Books":
    st.header("⏳ Currently Unreturned Books")
    unreturned = pd.read_sql("SELECT * FROM gold_unreturned_books", conn)
    st.dataframe(unreturned)

conn.close()
