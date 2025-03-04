from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from author.models import User, Author
from post.models import Post
from comment.models import Comment


class PostViewSetTests(APITestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword123'
        )
        
        # Create author
        self.author = Author.objects.create(
            name='Test Author',
            email='testauthor@example.com',
            user=self.user
        )
        
        # Create test post
        self.post = Post.objects.create(
            title='Test Post',
            content='This is a test post content',
            author=self.author,
            status='published',
            active=True
        )
        
        # Set up client and authenticate
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        # URLs
        self.list_url = reverse('post-list')
        self.detail_url = reverse('post-detail', kwargs={'pk': self.post.pk})
        self.add_comment_url = reverse('post-add-comment', kwargs={'pk': self.post.pk})
    
    def test_list_posts(self):
        """Test retrieving a list of posts"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_retrieve_post(self):
        """Test retrieving a single post"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.post.title)
        self.assertEqual(response.data['content'], self.post.content)
        self.assertEqual(response.data['author_name'], self.author.name)
    
    def test_create_post(self):
        """Test creating a new post"""
        data = {
            'title': 'New Test Post',
            'content': 'This is a new test post content',
            'status': 'draft',
            'active': True
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)
        self.assertEqual(Post.objects.get(title='New Test Post').author, self.author)
    
    def test_create_post_without_author(self):
        """Test creating a post when user has no author profile"""
        # Create a new user without an author profile
        new_user = User.objects.create_user(
            email='newuser@example.com',
            password='newpassword123'
        )
        
        # Authenticate with the new user
        self.client.force_authenticate(user=new_user)
        
        data = {
            'title': 'Post Without Author',
            'content': 'This post is created by a user without an author profile',
            'status': 'draft',
            'active': True
        }
        
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check that an author was created
        self.assertTrue(Author.objects.filter(user=new_user).exists())
        new_author = Author.objects.get(user=new_user)
        self.assertEqual(new_author.email, new_user.email)
        
        # Check that the post was created with the new author
        post = Post.objects.get(title='Post Without Author')
        self.assertEqual(post.author, new_author)
    
    def test_update_post(self):
        """Test updating a post"""
        data = {
            'title': 'Updated Test Post',
            'content': 'This is updated content',
            'status': 'published',
            'active': True
        }
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Test Post')
        self.assertEqual(self.post.content, 'This is updated content')
    
    def test_partial_update_post(self):
        """Test partially updating a post"""
        data = {
            'title': 'Partially Updated Post'
        }
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Partially Updated Post')
        # Content should remain unchanged
        self.assertEqual(self.post.content, 'This is a test post content')
    
    def test_delete_post(self):
        """Test deleting a post"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)
    
    def test_add_comment(self):
        """Test adding a comment to a post"""
        data = {
            'content': 'This is a test comment'
        }
        response = self.client.post(self.add_comment_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check that the comment was created
        self.assertEqual(Comment.objects.count(), 1)
        comment = Comment.objects.first()
        self.assertEqual(comment.content, 'This is a test comment')
        self.assertEqual(comment.user, self.user)
        self.assertEqual(comment.post, self.post)
    
    def test_add_invalid_comment(self):
        """Test adding an invalid comment to a post"""
        data = {
            'content': ''  # Empty content should be invalid
        }
        response = self.client.post(self.add_comment_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 0)
    
    def test_unauthenticated_access(self):
        """Test that unauthenticated users cannot access the API"""
        # Logout
        self.client.force_authenticate(user=None)
        
        # Try to list posts
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Try to create a post
        data = {
            'title': 'Unauthorized Post',
            'content': 'This should not be created',
            'status': 'draft',
            'active': True
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Try to add a comment
        data = {
            'content': 'Unauthorized comment'
        }
        response = self.client.post(self.add_comment_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
