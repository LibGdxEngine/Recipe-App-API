from rest_framework import serializers
from core.models import TagModel


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag objects"""

    class Meta():
        model = TagModel()
        fields = ('id', 'name',)
        read_only_fields = ('id',)
