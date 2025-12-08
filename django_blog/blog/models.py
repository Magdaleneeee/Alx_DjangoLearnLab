from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Tag(models.Model):
    """
    Tag model used to categorize posts.
    Each tag has a unique name.
    A Tag can be attached to many posts (many-to-many).
    """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    """
    Blog post model:
      - title: post title
      - content: full body text
      - published_date: timestamp when created
      - author: FK to User; one user can have many posts
      - tags: many-to-many relationship to Tag
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
        Used by generic views to know where to redirect
        after create/update.
        """
        return reverse('post-detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    """
    Comment model attached to a specific Post.
    - post: FK to Post (many comments per post)
    - author: FK to User (many comments per user)
    - content: the comment text
    - created_at: when comment was created
    - updated_at: when comment was last edited
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"

    def get_absolute_url(self):
        """
        After creating/updating/deleting a comment,
        go back to the post detail page.
        """
        return self.post.get_absolute_url()
