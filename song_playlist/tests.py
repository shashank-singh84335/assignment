from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Song
import os
import json

class SongModelTest(TestCase):
    def setUp(self):
        Song.objects.create(
            song_id='test123',
            title='Test Song',
            danceability=0.5,
            energy=0.7,
            key=1,
            loudness=-7.0,
            mode=1,
            acousticness=0.1,
            tempo=120.0,
            duration_ms=200000,
            num_bars=80,
            num_sections=8,
            num_segments=800
        )

    def test_song_creation(self):
        song = Song.objects.get(song_id='test123')
        self.assertEqual(song.title, 'Test Song')
        self.assertEqual(song.danceability, 0.5)
        self.assertEqual(song.energy, 0.7)
        
class SongAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.song1 = Song.objects.create(
            song_id='test123',
            title='Test Song',
            danceability=0.5,
            energy=0.7
        )
        self.song2 = Song.objects.create(
            song_id='test456',
            title='Another Test',
            danceability=0.6,
            energy=0.8
        )
        self.song_url = reverse('song-list')
        
    def test_get_all_songs(self):
        response = self.client.get(self.song_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        
    def test_search_by_title(self):
        response = self.client.get(f"{self.song_url}?title=Another")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Another Test')
        
    def test_rate_song(self):
        url = reverse('song-rate', kwargs={'pk': self.song1.id})
        response = self.client.post(url, {'rating': 5})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.song1.refresh_from_db()
        self.assertEqual(self.song1.rating, 5)
        
class DataProcessingTest(TestCase):
    def test_json_normalization(self):
        from .data_processor import normalize_data
        
        # Create a test JSON file
        test_data = {
            "id": {
                "0": "test123",
                "1": "test456"
            },
            "title": {
                "0": "Test Song",
                "1": "Another Test" 
            },
            "danceability": {
                "0": 0.5,
                "1": 0.6
            }
        }
        
        # Save test data to a temporary file
        test_file = 'test_data.json'
        with open(test_file, 'w') as f:
            json.dump(test_data, f)
        
        # Process the test file
        try:
            songs_created = normalize_data(test_file)
            self.assertEqual(songs_created, 2)
            
            # Check if songs were created correctly
            song1 = Song.objects.get(song_id='test123')
            self.assertEqual(song1.title, 'Test Song')
            self.assertEqual(song1.danceability, 0.5)
            
            song2 = Song.objects.get(song_id='test456')
            self.assertEqual(song2.title, 'Another Test')
            self.assertEqual(song2.danceability, 0.6)
        finally:
            # Clean up
            if os.path.exists(test_file):
                os.remove(test_file)
