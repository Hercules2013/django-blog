from django.urls import path

from blogposts.views import BlogPostViewSet

urlpatterns = [
    path(
        "",
        BlogPostViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
        name="blogpost-list",
    ),
    path(
        "<int:pk>/",
        BlogPostViewSet.as_view(
            {
                "get": "retrieve",
                "put": "partial_update",
                "delete": "destroy",
            }
        ),
        name="blogpost-detail",
    ),
]
