from django.db import models
from django.contrib.auth import get_user_model

class BlogPost(models.Model):
    """Basic model for a Blog Post"""
    
    title = models.CharField(max_length=50, blank=True)  # Allow blank titles
    content = models.TextField()  # Use TextField for content to handle large text
    # It's best practice not to delete users but to deactivate them, use SET_NULL on delete.
    author = models.ForeignKey(get_user_model(), null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title or "Untitled"
