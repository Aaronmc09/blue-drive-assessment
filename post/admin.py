from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'published_date', 'active')
    list_filter = ('status', 'published_date', 'author', 'active')
    search_fields = ('title', 'content')
    raw_id_fields = ('author',)
    date_hierarchy = 'published_date'
    ordering = ('status', '-published_date')
