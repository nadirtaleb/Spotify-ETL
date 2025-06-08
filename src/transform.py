import pandas as pd
from datetime import datetime, timedelta

class DataTransformer:
    def __init__(self):
        self.required_columns = [
            'id', 'name', 'artist', 'album', 'played_at',
            'duration_ms', 'popularity', 'danceability', 'energy',
            'key', 'loudness', 'mode', 'speechiness', 'acousticness',
            'instrumentalness', 'liveness', 'valence', 'tempo'
        ]

    def validate_data(self, df):
        """Validate the input DataFrame."""
        if df.empty:
            return False, "Empty DataFrame"

        # Check for required columns
        missing_columns = set(self.required_columns) - set(df.columns)
        if missing_columns:
            return False, f"Missing required columns: {missing_columns}"

        # Check for null values in critical columns
        critical_columns = ['id', 'name', 'artist', 'album', 'played_at']
        null_counts = df[critical_columns].isnull().sum()
        if null_counts.any():
            return False, f"Null values found in critical columns: {null_counts[null_counts > 0]}"

        # Validate timestamp format
        if not all(isinstance(x, datetime) for x in df['played_at']):
            return False, "Invalid timestamp format in played_at column"

        return True, "Data validation successful"

    def remove_duplicates(self, df):
        """Remove duplicate tracks based on id and played_at."""
        return df.drop_duplicates(subset=['id', 'played_at'], keep='first')

    def handle_missing_values(self, df):
        """Handle missing values in the DataFrame."""
        # Fill missing numeric values with 0
        numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
        df[numeric_columns] = df[numeric_columns].fillna(0)

        # Fill missing string values with 'Unknown'
        string_columns = df.select_dtypes(include=['object']).columns
        df[string_columns] = df[string_columns].fillna('Unknown')

        return df

    def transform_data(self, df):
        """Apply all transformations to the DataFrame."""
        # Validate data
        is_valid, message = self.validate_data(df)
        if not is_valid:
            raise ValueError(f"Data validation failed: {message}")

        # Remove duplicates
        df = self.remove_duplicates(df)

        # Handle missing values
        df = self.handle_missing_values(df)

        # Sort by played_at
        df = df.sort_values('played_at', ascending=False)

        return df 