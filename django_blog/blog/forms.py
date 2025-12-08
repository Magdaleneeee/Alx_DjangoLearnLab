from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from taggit.forms import TagWidget

from .models import Post, Comment


class CustomUserCreationForm(UserCreationForm):
    """
    Extends Django's UserCreationForm to include an email field.
    """
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
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
        fields = ("username", "email")


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
            'tags': TagWidget(),   
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

    class Meta:
        model = Comment
        fields = ("content",)
        widgets = {
            "content": forms.Textarea(attrs={"rows": 3}),
        }
