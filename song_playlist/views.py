from django.shortcuts import render
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Song
from .serializers import SongSerializer, SongRatingSerializer
import logging

# Set up logger
logger = logging.getLogger('song_playlist')

# Create your views here.

class SongPagination(PageNumberPagination):
    """
    Custom pagination class for Song viewset.
    
    This pagination class provides customization for how song data is paginated
    in the API responses, allowing clients to specify page size and handling
    maximum page size limits.
    
    Attributes:
        page_size (int): Default number of items per page
        page_size_query_param (str): Query parameter name to customize page size
        max_page_size (int): Maximum allowable page size
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class SongViewSet(viewsets.ModelViewSet):
    """
    API viewset for managing songs.
    
    This viewset provides CRUD operations for Song objects, along with
    additional functionality like searching by title and rating songs.
    
    Attributes:
        queryset: The base queryset of all Songs
        serializer_class: The serializer class for Song objects
        pagination_class: The pagination class to use
        filter_backends: List of filter backends to use
        search_fields: Fields to search when using SearchFilter
    """
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    pagination_class = SongPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
    
    def get_queryset(self):
        """
        Get the queryset of songs, optionally filtered by title.
        
        This method allows filtering the songs by title using a query parameter.
        If the 'title' parameter is provided, only songs with matching titles
        (case-insensitive partial match) are returned.
        
        Returns:
            QuerySet: Filtered queryset of Song objects
        """
        queryset = Song.objects.all()
        logger.debug(f"Initial queryset count: {queryset.count()}")
        
        title = self.request.query_params.get('title', None)
        if title is not None:
            logger.info(f"Filtering songs by title: {title}")
            logger.debug(f"Request params: {self.request.query_params}")
            queryset = queryset.filter(title__icontains=title)
            logger.debug(f"Filtered queryset count: {queryset.count()}")
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        """
        List all songs with optional filtering.
        
        This method overrides the default list implementation to add logging.
        
        Returns:
            Response: List of songs, possibly filtered
        """
        logger.info(f"Listing songs with params: {request.query_params}")
        logger.debug(f"Request headers: {request.headers}")
        response = super().list(request, *args, **kwargs)
        logger.debug(f"Response status: {response.status_code}, Results count: {len(response.data['results'])}")
        return response
    
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific song by ID.
        
        Returns:
            Response: Song detail information
        """
        logger.info(f"Retrieving song with pk: {kwargs.get('pk')}")
        logger.debug(f"Request method: {request.method}")
        response = super().retrieve(request, *args, **kwargs)
        song_data = response.data
        logger.debug(f"Retrieved song: {song_data['title']} (ID: {song_data['id']})")
        return response
    
    def create(self, request, *args, **kwargs):
        """
        Create a new song.
        
        Returns:
            Response: Created song data
        """
        logger.info(f"Creating new song: {request.data.get('title', 'Unknown')}")
        logger.debug(f"Request data: {request.data}")
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        """
        Update a song.
        
        Returns:
            Response: Updated song data
        """
        song = self.get_object()
        logger.info(f"Updating song: {song.title} (ID: {song.id})")
        logger.debug(f"Request data: {request.data}")
        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        """
        Partially update a song.
        
        Returns:
            Response: Updated song data
        """
        song = self.get_object()
        logger.info(f"Partially updating song: {song.title} (ID: {song.id})")
        logger.debug(f"Request data: {request.data}")
        return super().partial_update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """
        Delete a song.
        
        Returns:
            Response: Success response
        """
        song = self.get_object()
        logger.info(f"Deleting song: {song.title} (ID: {song.id})")
        logger.debug(f"Request method: {request.method}")
        return super().destroy(request, *args, **kwargs)
    
    @action(detail=True, methods=['post'], serializer_class=SongRatingSerializer)
    def rate(self, request, pk=None):
        """
        Rate a song by assigning a star rating.
        
        This action allows users to rate a song using a star rating system (0-5).
        The rating is saved to the song's rating field.
        
        Args:
            request: The HTTP request
            pk: The primary key of the song to rate
            
        Returns:
            Response: Success or error message
        """
        song = self.get_object()
        logger.debug(f"Rating song: {song.title} (ID: {song.id}), Current rating: {song.rating}")
        logger.debug(f"Request data: {request.data}")
        
        serializer = SongRatingSerializer(data=request.data)
        
        logger.info(f"Rating song '{song.title}' (ID: {song.id})")
        
        if serializer.is_valid():
            rating = serializer.validated_data['rating']
            logger.info(f"Setting rating to {rating}")
            logger.debug(f"Previous rating: {song.rating}, New rating: {rating}")
            song.rating = rating
            song.save()
            return Response({'status': 'song rated'})
        else:
            logger.error(f"Invalid rating data: {serializer.errors}")
            logger.debug(f"Validation errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
