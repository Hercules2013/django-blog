from rest_framework.viewsets import ModelViewSet
from blogposts.serializers import BlogPostSerializer
from blogposts.models import BlogPost
from rest_framework.permissions import IsAuthenticated


class BlogPostViewSet(ModelViewSet):
    serializer_class = BlogPostSerializer
    queryset = BlogPost.objects.all()
    permission_classes = [IsAuthenticated]
