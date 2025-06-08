import sqlite3
import kagglehub
import random
from datetime import datetime, timedelta

def download_dataset_from_kagglehub(name="jealousleopard/goodreadsbooks"):
    # Download latest version
    path = kagglehub.dataset_download(name)
    print("Path to dataset files:", path)
    return path


def create_sqlite_dataset(db_name="library.db"):
    # Connect to or create the database
    conn = sqlite3.connect(db_name)

    # Create a cursor to execute SQL
    cursor = conn.cursor()
    return conn, cursor


def generate_member(total=10):
    # First and last name samples
    first_names = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Hassan", "Ivy", "John"]
    last_names = ["Smith", "Jones", "Brown", "Taylor", "Wilson", "Walker", "Evans", "Thomas", "Roberts", "White"]

    members = []
    for _ in range(total):
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        join_date = datetime.today() - timedelta(days=random.randint(30, 365))
        members.append((name, join_date.date()))
    return members


def generate_borrowing_records(book_ids, member_ids):
    borrowing_records = []

    for member_id in member_ids:
        for _ in range(random.randint(1, 3)):
            book_id = random.choice(book_ids)
            borrow_days_ago = random.randint(5, 90)
            borrow_date = datetime.today() - timedelta(days=borrow_days_ago)

            # Randomly decide if the book was returned (70% chance)
            if random.random() < 0.7:
                return_date = borrow_date + timedelta(days=random.randint(5, 30))
                return_date = return_date.date()
            else:
                return_date = None  # Not yet returned

            borrowing_records.append((book_id, member_id, borrow_date.date(), return_date))

    return borrowing_records
