from django.contrib import admin
from .models import Author

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'user')
    search_fields = ('name', 'email', 'user__username', 'user__email')
    raw_id_fields = ('user',)
