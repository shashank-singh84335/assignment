"""
URL configuration for the song_playlist application.

This module defines the URL patterns for the song_playlist API,
using Django REST Framework's router to generate URLs for the viewsets.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SongViewSet

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'songs', SongViewSet)

# The API URLs are determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
] 