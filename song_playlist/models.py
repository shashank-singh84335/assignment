from django.db import models

# Create your models here.

class Song(models.Model):
    """
    Model representing a song with its various audio features and metadata.
    
    This model stores normalized data from audio analysis of songs, including
    attributes like danceability, energy, tempo, etc. It also includes a user
    rating field for song rating functionality.
    
    Attributes:
        song_id (CharField): Unique identifier for the song, usually from a streaming service
        title (CharField): The title of the song
        danceability (FloatField): Describes how suitable a track is for dancing (0.0 to 1.0)
        energy (FloatField): Represents the intensity and activity of the song (0.0 to 1.0)
        key (IntegerField): The key the track is in (0-11, where 0=C, 1=C#, etc.)
        loudness (FloatField): Overall loudness in decibels (dB)
        mode (IntegerField): Major (1) or minor (0) modality of the track
        acousticness (FloatField): Confidence measure of whether the track is acoustic (0.0 to 1.0)
        instrumentalness (FloatField): Predicts whether a track has no vocals (0.0 to 1.0)
        liveness (FloatField): Presence of an audience in the recording (0.0 to 1.0)
        valence (FloatField): The musical positiveness conveyed by a track (0.0 to 1.0)
        tempo (FloatField): The overall estimated tempo in beats per minute (BPM)
        duration_ms (IntegerField): The duration of the track in milliseconds
        time_signature (IntegerField): The estimated time signature (beats per bar)
        num_bars (IntegerField): The number of bars in the track
        num_sections (IntegerField): The number of sections in the track
        num_segments (IntegerField): The number of segments in the track
        rating (IntegerField): User-assigned rating of the song (0-5 stars)
    """
    song_id = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    danceability = models.FloatField(null=True, blank=True)
    energy = models.FloatField(null=True, blank=True)
    key = models.IntegerField(null=True, blank=True)
    loudness = models.FloatField(null=True, blank=True)
    mode = models.IntegerField(null=True, blank=True)
    acousticness = models.FloatField(null=True, blank=True)
    instrumentalness = models.FloatField(null=True, blank=True)
    liveness = models.FloatField(null=True, blank=True)
    valence = models.FloatField(null=True, blank=True)
    tempo = models.FloatField(null=True, blank=True)
    duration_ms = models.IntegerField(null=True, blank=True)
    time_signature = models.IntegerField(null=True, blank=True)
    num_bars = models.IntegerField(null=True, blank=True)
    num_sections = models.IntegerField(null=True, blank=True)
    num_segments = models.IntegerField(null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True, default=0)
    
    def __str__(self):
        """Return a string representation of the song."""
        return self.title
