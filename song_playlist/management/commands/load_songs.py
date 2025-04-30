from django.core.management.base import BaseCommand
from song_playlist.data_processor import load_data_from_command
import logging
import time

logger = logging.getLogger('song_playlist')

class Command(BaseCommand):
    """
    Django management command to load song data from a JSON file.
    
    This command imports song data from a JSON file into the database.
    It normalizes the nested JSON structure and creates Song model instances.
    """
    help = 'Load songs data from JSON file'

    def handle(self, *args, **options):
        """
        Execute the command to load songs data.
        
        This method is called when the management command is executed.
        It logs the start and end of the data import process, along with
        the number of songs created.
        
        Args:
            *args: Variable length argument list
            **options: Arbitrary keyword arguments
        """
        logger.info("Starting data import management command")
        self.stdout.write(self.style.SUCCESS('Starting data import...'))
        
        start_time = time.time()
        logger.debug(f"Start time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}")
        
        try:
            # Get song count before import
            from song_playlist.models import Song
            song_count_before = Song.objects.count()
            logger.debug(f"Song count before import: {song_count_before}")
            
            # Import songs
            songs_created = load_data_from_command()
            
            # Get song count after import
            song_count_after = Song.objects.count()
            logger.debug(f"Song count after import: {song_count_after}")
            logger.debug(f"Difference: {song_count_after - song_count_before}")
            
            end_time = time.time()
            duration = end_time - start_time
            logger.debug(f"End time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))}")
            logger.debug(f"Duration: {duration:.2f} seconds")
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully imported {songs_created} songs in {duration:.2f} seconds')
            )
            logger.info(f"Data import completed successfully: {songs_created} songs created in {duration:.2f} seconds")
        except Exception as e:
            end_time = time.time()
            duration = end_time - start_time
            logger.debug(f"End time (error): {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))}")
            logger.debug(f"Duration until error: {duration:.2f} seconds")
            
            self.stdout.write(
                self.style.ERROR(f'Error importing songs: {e}')
            )
            logger.error(f"Data import failed after {duration:.2f} seconds: {e}")
            logger.exception("Detailed traceback:")
            raise 