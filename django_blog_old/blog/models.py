from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    """
    Simple blog post model.
    - title: post headline
    - content: main body text
    - published_date: timestamp when post is created
    - author: link to Django's built-in User; a user can have many posts
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )

    def __str__(self) -> str:
        return self.title
