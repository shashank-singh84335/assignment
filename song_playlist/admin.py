from django.contrib import admin
from .models import Song

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Song model.
    
    This class configures how Song objects are displayed and managed in the Django admin interface.
    
    Attributes:
        list_display: Fields to display in the list view
        search_fields: Fields to include in the search functionality
        list_filter: Fields to use for filtering the list view
    """
    list_display = ('title', 'song_id', 'rating')
    search_fields = ('title', 'song_id')
    list_filter = ('rating',)
