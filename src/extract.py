import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime, timedelta
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

class SpotifyExtractor:
    def __init__(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=os.getenv('SPOTIFY_CLIENT_ID'),
            client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
            redirect_uri=os.getenv('SPOTIFY_REDIRECT_URI'),
            scope='user-read-recently-played'
        ))

    def get_recently_played(self, limit=50):
        """Fetch recently played tracks from Spotify API."""
        try:
            results = self.sp.current_user_recently_played(limit=limit)
            return results['items']
        except Exception as e:
            print(f"Error fetching recently played tracks: {e}")
            return []

    def get_audio_features(self, track_ids):
        """Fetch audio features for a list of track IDs."""
        try:
            features = self.sp.audio_features(track_ids)
            return features
        except Exception as e:
            print(f"Error fetching audio features: {e}")
            return []

    def extract_data(self):
        """Extract and combine recently played tracks with their audio features."""
        # Get recently played tracks
        recent_tracks = self.get_recently_played()
        
        if not recent_tracks:
            return pd.DataFrame()

        # Prepare track data
        tracks_data = []
        for item in recent_tracks:
            track = item['track']
            played_at = datetime.strptime(item['played_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
            
            track_info = {
                'id': track['id'],
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'album': track['album']['name'],
                'played_at': played_at,
                'duration_ms': track['duration_ms'],
                'popularity': track['popularity']
            }
            tracks_data.append(track_info)

        # Get audio features for all tracks
        track_ids = [track['id'] for track in tracks_data]
        audio_features = self.get_audio_features(track_ids)

        # Combine track data with audio features
        for track, features in zip(tracks_data, audio_features):
            if features:
                track.update({
                    'danceability': features['danceability'],
                    'energy': features['energy'],
                    'key': features['key'],
                    'loudness': features['loudness'],
                    'mode': features['mode'],
                    'speechiness': features['speechiness'],
                    'acousticness': features['acousticness'],
                    'instrumentalness': features['instrumentalness'],
                    'liveness': features['liveness'],
                    'valence': features['valence'],
                    'tempo': features['tempo']
                })

        return pd.DataFrame(tracks_data) 