import pandas as pd
from src.data.dataset_utils import create_sqlite_dataset


class GoldETL:
    """
    ETL class for aggregating and exposing high-value analytics (Gold layer).
    """

    def __init__(self, sql_db_name="library.db"):
        self.sql_db_name = sql_db_name
        self.conn, self.cursor = create_sqlite_dataset(self.sql_db_name)

    def create_top_books_table(self, min_rating=4.5, limit=20):
        """
        Creates a table of top-rated books from the Silver layer.
        """
        query = f"""
            CREATE TABLE IF NOT EXISTS gold_top_books AS
            SELECT 
                Title, 
                Author, 
                YearPublished, 
                AvgRating
            FROM silver_books
            WHERE AvgRating >= {min_rating}
            ORDER BY AvgRating DESC
            LIMIT {limit};
        """
        self.cursor.execute(query)
        self.conn.commit()

    def create_top_borrowed_books_view(self):
        """
        Creates a view of the top 10 most borrowed books.
        """
        self.cursor.execute("""
            CREATE VIEW IF NOT EXISTS gold_top_borrowed_books AS
            SELECT 
                book.Title, 
                book.Author, 
                COUNT(*) AS BorrowCount
            FROM BorrowingRecords AS borrow
            JOIN silver_books AS book 
                ON borrow.BookID = book.BookID
            GROUP BY borrow.BookID
            ORDER BY BorrowCount DESC
            LIMIT 10;
        """)
        self.conn.commit()

    def create_unreturned_books_view(self):
        """
        Creates a view of currently unreturned borrowed books.
        """
        self.cursor.execute("""
            CREATE VIEW IF NOT EXISTS gold_unreturned_books AS
            SELECT 
                member.Name AS Borrower,
                book.Title,
                borrow.BorrowDate,
                JULIANDAY('now') - JULIANDAY(borrow.BorrowDate) AS DaysOut,
                CASE 
                    WHEN JULIANDAY('now') - JULIANDAY(borrow.BorrowDate) > 14 THEN 'Yes'
                    ELSE 'No'
                END AS IsOverdue
            FROM BorrowingRecords AS borrow
            JOIN Members AS member 
                ON borrow.MemberID = member.MemberID
            JOIN silver_books AS book 
                ON borrow.BookID = book.BookID
            WHERE borrow.ReturnDate IS NULL;
        """)
        self.conn.commit()

    def create_monthly_borrowing_view(self):
        """
        Creates a view showing borrowing trends by month.
        """
        self.cursor.execute("""
            CREATE VIEW IF NOT EXISTS gold_monthly_borrowing AS
            SELECT 
                strftime('%Y-%m', BorrowDate) AS Month,
                COUNT(*) AS BorrowCount
            FROM BorrowingRecords
            GROUP BY Month
            ORDER BY Month ASC;
        """)
        self.conn.commit()

    def preview_gold_outputs(self):
        """
        Previews each gold-level table/view.
        """
        print("Top Rated Books:")
        print(pd.read_sql_query("SELECT * FROM gold_top_books LIMIT 5;", self.conn))

        print("\nTop Borrowed Books:")
        print(pd.read_sql_query("SELECT * FROM gold_top_borrowed_books;", self.conn))

        print("\nUnreturned Books:")
        print(pd.read_sql_query("SELECT * FROM gold_unreturned_books;", self.conn))

        print("\nMonthly Borrowing Stats:")
        print(pd.read_sql_query("SELECT * FROM gold_monthly_borrowing;", self.conn))
