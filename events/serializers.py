from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Event, Review, Category, Tag, MediaBlob

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']

class MediaBlobSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    class Meta:
        model = MediaBlob
        fields = ['id', 'filename', 'content_type', 'size', 'url']
    def get_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.get_absolute_url()) if hasattr(obj, 'get_absolute_url') else ''

class EventSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField()
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(source='category', queryset=Category.objects.all(), write_only=True)
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(source='tags', many=True, queryset=Tag.objects.all(), write_only=True, required=False)
    avg_rating = serializers.FloatField(read_only=True)
    media = MediaBlobSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = [
            'id','slug','title','description','creator','category','category_id','tags','tag_ids','start_datetime','end_datetime','price','is_free','venue_name','address','city','latitude','longitude','capacity','status','featured','avg_rating','media'
        ]

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        fields = ['id', 'event', 'user', 'rating', 'comment', 'created_at']
        read_only_fields = ['user']
