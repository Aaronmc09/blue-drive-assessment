from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/posts/", include("post.urls")),
    path("auth/", include("django.contrib.auth.urls")),
]
