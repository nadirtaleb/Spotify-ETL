# Spotify ETL Pipeline

This project implements an ETL (Extract, Transform, Load) pipeline for Spotify listening data. It automatically fetches your recently played tracks, enriches them with audio features, and stores them in a SQLite database.

## Features

- Automated extraction of recently played tracks via Spotify API
- Data transformation and enrichment with audio features
- Duplicate detection and removal
- Data quality checks
- Automated nightly runs via GitHub Actions
- Containerized with Docker
- Comprehensive test coverage

## Prerequisites

- Python 3.8+
- Spotify Developer Account
- Docker and Docker Compose (for containerized deployment)

## Setup

1. Create a Spotify Developer account and create a new application at https://developer.spotify.com/dashboard
2. Get your Client ID and Client Secret
3. Create a `.env` file with the following variables:
   ```
   SPOTIFY_CLIENT_ID=your_client_id
   SPOTIFY_CLIENT_SECRET=your_client_secret
   SPOTIFY_REDIRECT_URI=http://localhost:8888/callback
   ```

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/spotify-etl.git
cd spotify-etl

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Local Development

```bash
python src/main.py
```

### Docker

```bash
docker-compose up
```

## Project Structure

```
spotify-etl/
├── src/
│   ├── main.py           # Main ETL pipeline
│   ├── extract.py        # Spotify API interaction
│   ├── transform.py      # Data transformation logic
│   ├── load.py          # Database operations
│   └── models.py        # SQLAlchemy models
├── tests/
│   ├── test_extract.py
│   ├── test_transform.py
│   └── test_load.py
├── .github/
│   └── workflows/
│       └── etl.yml      # GitHub Actions workflow
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

## Testing

```bash
pytest tests/
```

## License

MIT 