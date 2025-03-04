from django.db import models
from author.models import Author

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('draft', 'Draft'), ('published', 'Published')])
    active = models.BooleanField()

    def __str__(self):
        return self.title
