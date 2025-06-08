import pytest
import pandas as pd
from datetime import datetime
from src.transform import DataTransformer

@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'id': ['track1', 'track2'],
        'name': ['Song 1', 'Song 2'],
        'artist': ['Artist 1', 'Artist 2'],
        'album': ['Album 1', 'Album 2'],
        'played_at': [datetime.now(), datetime.now()],
        'duration_ms': [180000, 240000],
        'popularity': [80, 90],
        'danceability': [0.8, 0.7],
        'energy': [0.9, 0.8],
        'key': [1, 2],
        'loudness': [-5.0, -6.0],
        'mode': [1, 0],
        'speechiness': [0.1, 0.2],
        'acousticness': [0.3, 0.4],
        'instrumentalness': [0.5, 0.6],
        'liveness': [0.7, 0.8],
        'valence': [0.9, 0.8],
        'tempo': [120.0, 130.0]
    })

def test_validate_data(sample_data):
    transformer = DataTransformer()
    is_valid, message = transformer.validate_data(sample_data)
    assert is_valid
    assert message == "Data validation successful"

def test_remove_duplicates(sample_data):
    transformer = DataTransformer()
    # Add a duplicate row
    sample_data = pd.concat([sample_data, sample_data.iloc[0:1]])
    result = transformer.remove_duplicates(sample_data)
    assert len(result) == 2  # Should have removed the duplicate

def test_handle_missing_values(sample_data):
    transformer = DataTransformer()
    # Add some missing values
    sample_data.loc[0, 'danceability'] = None
    sample_data.loc[0, 'name'] = None
    result = transformer.handle_missing_values(sample_data)
    assert result['danceability'].isnull().sum() == 0
    assert result['name'].isnull().sum() == 0
    assert result.loc[0, 'danceability'] == 0
    assert result.loc[0, 'name'] == 'Unknown' 