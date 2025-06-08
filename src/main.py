import os
from datetime import datetime, timedelta
from extract import SpotifyExtractor
from transform import DataTransformer
from load import DataLoader
from dotenv import load_dotenv

load_dotenv()

def run_etl():
    """Run the complete ETL pipeline."""
    print(f"Starting ETL pipeline at {datetime.now()}")
    
    try:
        # Initialize components
        extractor = SpotifyExtractor()
        transformer = DataTransformer()
        loader = DataLoader()

        # Extract data
        print("Extracting data from Spotify...")
        df = extractor.extract_data()
        
        if df.empty:
            print("No new data to process")
            return

        # Transform data
        print("Transforming data...")
        df = transformer.transform_data(df)

        # Load data
        print("Loading data to database...")
        loader.load_data(df)

        print(f"ETL pipeline completed successfully at {datetime.now()}")
        
    except Exception as e:
        print(f"Error in ETL pipeline: {e}")
        raise

if __name__ == "__main__":
    run_etl() 