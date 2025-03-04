from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'published_date', 'status', 'active', 'author_name', 'comments']
        read_only_fields = ['id', 'published_date', 'comments'] 
    
    author_name = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    
    def get_author_name(self, obj):
        return obj.author.name
    
    def get_comments(self, obj):
        return PostCommentSerializer(obj.comments.all(), many=True).data

class PostCommentSerializer(serializers.Serializer):
    class Meta:
        fields = ['content', 'created', 'user']

    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField(read_only=True)
    user = serializers.CharField(source='user.email', read_only=True)