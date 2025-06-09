import pandas as pd
from src.data.dataset_utils import create_sqlite_dataset, generate_member, generate_borrowing_records


class SilverETL:
    """
    ETL class for processing and storing cleaned (Silver layer) data into SQLite.
    """

    def __init__(self, sql_db_name="library.db"):
        self.sql_db_name = sql_db_name
        self.conn, self.cursor = create_sqlite_dataset(self.sql_db_name)

    def transform_bronze_books(self):
        """
        Transforms bronze_books into silver_books with selected and cleaned columns.
        """
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS silver_books AS
            SELECT DISTINCT
                bookID AS BookID,
                TRIM(title) AS Title,
                TRIM(authors) AS Author,
                publication_date AS YearPublished,
                average_rating AS AvgRating
            FROM bronze_books
            WHERE title IS NOT NULL
            AND authors IS NOT NULL
            AND publication_date IS NOT NULL
            AND average_rating IS NOT NULL;
        """)
        self.conn.commit()

    def create_members_table(self, total_members=20):
        """
        Creates and populates the Members table with synthetic member data.
        """
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Members (
                MemberID 
                    INTEGER 
                    PRIMARY KEY 
                    AUTOINCREMENT,
                Name TEXT NOT NULL,
                JoinDate DATE DEFAULT (DATE('now'))
            );
            """)
        self.conn.commit()

        members = generate_member(total=total_members)
        self.cursor.executemany(
            "INSERT INTO Members (Name, JoinDate) VALUES (?, ?);",
            members
        )
        self.conn.commit()

    def create_borrowing_records_table(self):
        """
        Creates and populates BorrowingRecords table based on existing books and members.
        """
        book_ids = pd.read_sql_query("SELECT BookID FROM silver_books LIMIT 100;", self.conn)["BookID"].tolist()
        member_ids = pd.read_sql_query("SELECT MemberID FROM Members;", self.conn)["MemberID"].tolist()

        records = generate_borrowing_records(book_ids, member_ids)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS BorrowingRecords (
                RecordID 
                    INTEGER 
                    PRIMARY KEY 
                    AUTOINCREMENT,
                BookID INTEGER,
                MemberID INTEGER,
                BorrowDate 
                    DATE 
                    DEFAULT (DATE('now')),
                ReturnDate DATE,
                FOREIGN KEY (BookID) 
                    REFERENCES silver_books(BookID),
                FOREIGN KEY (MemberID) 
                    REFERENCES Members(MemberID)
            );
        """)
        self.conn.commit()

        self.cursor.executemany(
            """
            INSERT INTO BorrowingRecords (BookID, MemberID, BorrowDate, ReturnDate)
            VALUES (?, ?, ?, ?);
            """,
            records
        )
        self.conn.commit()

    def preview_tables(self):
        """
        Previews top 5 rows from each silver layer table.
        """
        print("silver_books:")
        print(pd.read_sql_query("SELECT * FROM silver_books LIMIT 5;", self.conn))

        print("\nMembers:")
        print(pd.read_sql_query("SELECT * FROM Members LIMIT 5;", self.conn))

        print("\nBorrowingRecords:")
        print(pd.read_sql_query("SELECT * FROM BorrowingRecords LIMIT 5;", self.conn))
