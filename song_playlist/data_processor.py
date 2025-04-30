import json
import pandas as pd
import logging
import os
from .models import Song

# Set up logger
logger = logging.getLogger('song_playlist')

def normalize_data(json_file_path):
    """
    Normalize the JSON data from a structured playlist file and create Song objects.
    
    This function processes a JSON file containing song data in a nested map format.
    It transforms the nested maps into a normalized table structure and creates or
    updates Song model instances in the database.
    
    Args:
        json_file_path (str): Path to the JSON file containing song data
    
    Returns:
        int: Number of songs successfully processed and created in the database
    
    Raises:
        FileNotFoundError: If the JSON file does not exist
        json.JSONDecodeError: If the JSON file is invalid
        Exception: For any other errors during processing
    """
    logger.info(f"Starting data normalization from {json_file_path}")
    logger.debug(f"File size: {os.path.getsize(json_file_path)} bytes")
    
    try:
        # Read JSON file
        with open(json_file_path, 'r') as f:
            data = json.load(f)
        
        logger.debug(f"Successfully loaded JSON data with {len(data)} attribute maps")
        logger.debug(f"Available attributes: {list(data.keys())}")
        
        # Convert to pandas DataFrame
        df = pd.DataFrame()
        
        # Initialize columns from the JSON data
        for key in data:
            df[key] = pd.Series(data[key])
            logger.debug(f"Added column '{key}' with {len(data[key])} values")
        
        # Ensure the dataframe is properly indexed
        df.reset_index(inplace=True)
        df.rename(columns={'index': 'idx'}, inplace=True)
        
        logger.debug(f"Normalized data into DataFrame with {len(df)} rows and {len(df.columns)} columns")
        logger.debug(f"DataFrame columns: {df.columns.tolist()}")
        logger.debug(f"First row sample: {df.iloc[0].to_dict() if not df.empty else 'No data'}")
        
        # Delete all existing songs before importing (optional)
        # Song.objects.all().delete()
        
        # Create Song objects
        songs_created = 0
        songs_updated = 0
        for idx, row in df.iterrows():
            try:
                if idx % 10 == 0:
                    logger.debug(f"Processing song {idx+1}/{len(df)}")
                
                song_id = row['id']
                song, created = Song.objects.update_or_create(
                    song_id=song_id,
                    defaults={
                        'title': row['title'] if 'title' in row else '',
                        'danceability': row.get('danceability'),
                        'energy': row.get('energy'),
                        'key': row.get('key'),
                        'loudness': row.get('loudness'),
                        'mode': row.get('mode'),
                        'acousticness': row.get('acousticness'),
                        'instrumentalness': row.get('instrumentalness'),
                        'liveness': row.get('liveness'),
                        'valence': row.get('valence'),
                        'tempo': row.get('tempo'),
                        'duration_ms': row.get('duration_ms'),
                        'time_signature': row.get('time_signature'),
                        'num_bars': row.get('num_bars'),
                        'num_sections': row.get('num_sections'),
                        'num_segments': row.get('num_segments'),
                    }
                )
                if created:
                    songs_created += 1
                    logger.debug(f"Created new song: {row.get('title', 'Unknown')} ({row.get('id', 'Unknown ID')})")
                else:
                    songs_updated += 1
                    logger.debug(f"Updated existing song: {row.get('title', 'Unknown')} ({row.get('id', 'Unknown ID')})")
            except Exception as e:
                logger.error(f"Error processing song {row.get('id', 'unknown')}: {e}")
                logger.exception("Detailed traceback:")
                print(f"Error processing song {row.get('id', 'unknown')}: {e}")
        
        logger.info(f"Completed data normalization. Created {songs_created} new songs, updated {songs_updated} existing songs.")
        return songs_created
    except FileNotFoundError:
        logger.error(f"JSON file not found: {json_file_path}")
        logger.exception("Detailed traceback:")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON format in file {json_file_path}: {e}")
        logger.exception("Detailed traceback:")
        raise
    except Exception as e:
        logger.error(f"Error during data normalization: {e}")
        logger.exception("Detailed traceback:")
        raise

def load_data_from_command():
    """
    Load song data from the default JSON file using the normalize_data function.
    
    This function is designed to be called from a Django management command.
    It locates the JSON file in the project root directory and calls normalize_data
    to process it.
    
    Returns:
        int: Number of songs successfully processed and created in the database
    
    Raises:
        Any exceptions raised by normalize_data
    """
    import os
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_file = os.path.join(base_dir, 'playlist.json')
    logger.info(f"Loading data from command using file: {json_file}")
    return normalize_data(json_file) 