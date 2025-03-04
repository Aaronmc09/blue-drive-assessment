from rest_framework import serializers
from .models import Post
from author.models import Author

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content', 'published_date', 'author_name']
        read_only_fields = ['published_date'] 
    
    author_name = serializers.SerializerMethodField()
    
    def get_author_name(self, obj):
        return obj.author.name
