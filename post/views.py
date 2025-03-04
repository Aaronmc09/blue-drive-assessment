from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import Post
from .serializers import PostSerializer, PostCommentSerializer
from author.models import Author
from comment.serializers import CommentSerializer

class PostViewSet(
    GenericViewSet,
    RetrieveModelMixin,
    ListModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin
):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def create_new_author(self, user):
        author = Author.objects.create(user=user, email=user.email)
        return author
    
    def perform_create(self, serializer):
        author = Author.objects.filter(user=self.request.user).first()
        if not author:
            author = self.create_new_author(self.request.user)
        serializer.save(author=author)
        
    @action(detail=True, methods=['post'], serializer_class=PostCommentSerializer)
    def add_comment(self, request, pk):
        serializer = PostCommentSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer = CommentSerializer(data={
                'content': serializer.validated_data['content'],
                'user': request.user.id,
                'post': pk
            })
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    