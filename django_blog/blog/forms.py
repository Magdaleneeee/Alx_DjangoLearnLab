from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Post, Comment, Tag


class CustomUserCreationForm(UserCreationForm):
    """
    Extends Django's UserCreationForm to include an email field.
    """
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    """
    Form for updating basic profile info (username + email).
    """
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email')


class PostForm(forms.ModelForm):
    """
    ModelForm for creating and updating blog posts.
    Author is set automatically in the views.

    'tags' is a simple CharField where the user can type
    comma-separated tag names. The view will handle creating
    Tag objects and associating them with the Post.
    """
    tags = forms.CharField(
        required=False,
        help_text="Comma-separated tags, e.g. django, python, web",
    )

    class Meta:
        model = Post
        fields = ('title', 'content', 'tags')


class CommentForm(forms.ModelForm):
    """
    ModelForm for creating/updating comments.
    Author and post are set in the view; only content is editable.
    """
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
        }
