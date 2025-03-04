from django.contrib import admin
from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created')
    list_filter = ('created',)
    search_fields = ('content', 'user__username', 'post__title')
    raw_id_fields = ('user', 'post')
    actions = ['approve_comments', 'disapprove_comments']

    def approve_comments(self, request, queryset):
        queryset.update(is_active=True)
    approve_comments.short_description = 'Approve selected comments'

    def disapprove_comments(self, request, queryset):
        queryset.update(is_active=False)
    disapprove_comments.short_description = 'Disapprove selected comments'
