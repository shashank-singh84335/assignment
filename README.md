# Song Playlist API

A Django REST API for managing song playlists with features for song data normalization, filtering, and rating.

## Features

- Data normalization from JSON to structured database format
- REST API with pagination for listing songs
- Song search by title
- Star rating system for songs
- Comprehensive logging
- Swagger/OpenAPI documentation

## Installation

### Prerequisites

- Python 3.11+
- pip (Python package installer)

### Setup

1. Clone the repository:
   ```
   git clone <repository-url>
   cd assignment
   ```

2. Set up a virtual environment:
   ```
   python -m venv env
   source env/bin/activate  # On Windows, use: env\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Apply database migrations:
   ```
   python manage.py migrate
   ```

5. Load sample data:
   ```
   python manage.py load_songs
   ```

## Usage

1. Run the development server:
   ```
   python manage.py runserver
   ```

2. Access the API:
   - API endpoints: http://127.0.0.1:8000/api/songs/
   - Admin interface: http://127.0.0.1:8000/admin/
   - Swagger UI: http://127.0.0.1:8000/swagger/
   - ReDoc: http://127.0.0.1:8000/redoc/

## API Endpoints

- `GET /api/songs/` - List all songs (with pagination)
- `GET /api/songs/?title=searchterm` - Search songs by title
- `GET /api/songs/{id}/` - Get a specific song by ID
- `POST /api/songs/{id}/rate/` - Rate a song (using a 0-5 star rating)

## Data Structure

The project uses the following data model:

- `Song`: Represents a song with various attributes including audio features and a user rating.

## Running Tests

Run the test suite:
```
python manage.py test
```

## Logging

The application includes detailed logging with SQL query tracking. All logs are written to a single file:
- `logs/application.log` - Contains both application logs and SQL queries in sequential order

This allows you to see the exact sequence of operations and corresponding database queries.

## License

This project is for demonstration purposes only. 