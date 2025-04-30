from rest_framework import serializers
from .models import Song

class SongSerializer(serializers.ModelSerializer):
    """
    Serializer for the Song model.
    
    This serializer handles the conversion between Song model instances and
    JSON representations. It includes all fields from the Song model.
    
    Meta:
        model: The model class to serialize
        fields: Fields to include in the serialization
    """
    class Meta:
        model = Song
        fields = '__all__'

class SongRatingSerializer(serializers.ModelSerializer):
    """
    Serializer for the rating field of the Song model.
    
    This serializer is used specifically for the song rating functionality,
    allowing users to submit a rating for a song. It only includes the rating field.
    
    Meta:
        model: The model class to serialize
        fields: Fields to include in the serialization (only 'rating')
    """
    class Meta:
        model = Song
        fields = ['rating']
        
    def validate_rating(self, value):
        """
        Validate the rating value.
        
        Args:
            value: The rating value to validate
            
        Returns:
            The validated value
            
        Raises:
            serializers.ValidationError: If the rating is not between 0 and 5
        """
        if value < 0 or value > 5:
            raise serializers.ValidationError("Rating must be between 0 and 5")
        return value 