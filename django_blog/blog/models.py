from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    """
    Blog post model:
      - title: short title for the post.
      - content: main body text.
      - published_date: timestamp when the post was created.
      - author: link to Django's built-in User; one user can have many posts.
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )

    def __str__(self):
        return self.title

def get_absolute_url(self):
        """
        Used by Django's generic CreateView/UpdateView to know where to redirect
        after successfully saving a Post.
        """
        return reverse('post-detail', kwargs={'pk': self.pk})