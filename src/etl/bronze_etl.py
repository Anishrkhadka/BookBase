import pandas as pd
from src.data.dataset_utils import download_dataset_from_kagglehub, create_sqlite_dataset


class BronzeETL:
    """
    ETL class for handling the ingestion of raw data (Bronze layer)
    into a SQLite database.
    """

    def __init__(self, 
                 dataset_location="jealousleopard/goodreadsbooks", 
                 dataset_name="books.csv",
                 sql_db_name="library.db"):
        self.dataset_location = dataset_location
        self.dataset_name = dataset_name
        self.sql_db_name = sql_db_name
        self.conn, self.cursor = create_sqlite_dataset(self.sql_db_name)
        self.dataset_path = None
        self.books_df = None

    def download_data(self):
        """Downloads dataset from KaggleHub and stores the path."""
        self.dataset_path = download_dataset_from_kagglehub(self.dataset_location)

    def load_raw_books(self):
        """Loads the books.csv file into a pandas DataFrame."""
        if not self.dataset_path:
            raise ValueError("Dataset path not set. Run download_data() first.")

        books_file = f"{self.dataset_path}/{self.dataset_name}"
        self.books_df = pd.read_csv(
            books_file,
            on_bad_lines='skip',
            quotechar='"',
            sep=","
        )
        print("Sample of raw books data:")
        print(self.books_df.sample(5))

    def write_to_sqlite(self, table_name="bronze_books"):
        """Writes the raw books DataFrame to a SQLite table."""
        if self.books_df is None:
            raise ValueError("Books DataFrame is empty. Run load_raw_books() first.")
        
        self.books_df.to_sql(table_name, self.conn, if_exists="replace", index=False)
        print(f"Data written to table: {table_name}")
