
from src.data.dataset_utils import delete_sqlit_database
delete_sqlit_database("library.db") #we delete any exiting dataset called library.db for clean start

from src.etl.bronze_etl import BronzeETL
from src.etl.silver_etl import SilverETL
from src.etl.gold_etl import GoldETL


def run_bronze_etl():
    bronze = BronzeETL()
    bronze.download_data()
    bronze.load_raw_books()
    bronze.write_to_sqlite()

def run_silver_etl():
    silver = SilverETL()
    silver.transform_bronze_books()
    silver.create_members_table(total_members=20)
    silver.create_borrowing_records_table()
    silver.preview_tables()


def run_gold_etl():
    gold = GoldETL()
    gold.create_top_books_table()
    gold.create_top_borrowed_books_view()
    gold.create_unreturned_books_view()
    gold.create_monthly_borrowing_view()
    gold.preview_gold_outputs()


def main():
    
    print("Running Bronze ETL...")
    run_bronze_etl()

    print("\nRunning Silver ETL...")
    run_silver_etl()

    print("\nRunning Gold ETL...")
    run_gold_etl()


if __name__ == "__main__":
    main()
