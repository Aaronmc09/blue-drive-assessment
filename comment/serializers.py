from rest_framework import serializers
from .models import Comment
from author.models import User
from post.serializers import PostSerializer

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content', 'user', 'post']
    
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    post = PostSerializer(read_only=True)