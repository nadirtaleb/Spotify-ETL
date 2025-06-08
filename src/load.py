from sqlalchemy.exc import SQLAlchemyError
from models import Track, init_db
import pandas as pd
from datetime import datetime

class DataLoader:
    def __init__(self, db_url='sqlite:///spotify_tracks.db'):
        self.Session = init_db(db_url)

    def load_data(self, df):
        """Load transformed data into the database."""
        if df.empty:
            print("No data to load")
            return

        session = self.Session()
        try:
            # Convert DataFrame rows to Track objects
            for _, row in df.iterrows():
                track = Track(
                    id=row['id'],
                    name=row['name'],
                    artist=row['artist'],
                    album=row['album'],
                    played_at=row['played_at'],
                    duration_ms=row['duration_ms'],
                    popularity=row['popularity'],
                    danceability=row['danceability'],
                    energy=row['energy'],
                    key=row['key'],
                    loudness=row['loudness'],
                    mode=row['mode'],
                    speechiness=row['speechiness'],
                    acousticness=row['acousticness'],
                    instrumentalness=row['instrumentalness'],
                    liveness=row['liveness'],
                    valence=row['valence'],
                    tempo=row['tempo']
                )
                
                # Check if track already exists
                existing_track = session.query(Track).filter_by(
                    id=track.id,
                    played_at=track.played_at
                ).first()
                
                if not existing_track:
                    session.add(track)

            session.commit()
            print(f"Successfully loaded {len(df)} tracks to database")
            
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error loading data to database: {e}")
            raise
        finally:
            session.close()

    def get_latest_track_time(self):
        """Get the timestamp of the most recent track in the database."""
        session = self.Session()
        try:
            latest_track = session.query(Track).order_by(Track.played_at.desc()).first()
            return latest_track.played_at if latest_track else None
        finally:
            session.close() 