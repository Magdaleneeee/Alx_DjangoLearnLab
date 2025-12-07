# blog/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import CustomUserCreationForm, UserUpdateForm


def index(request):
    """
    Simple home page for the blog.
    """
    return render(request, 'blog/index.html')


def register(request):
    """
    User registration view.
    Uses CustomUserCreationForm to create a new user with email.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created. You can now log in.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'blog/register.html', {'form': form})


@login_required
def profile(request):
    """
    Profile view: allows authenticated users to view and edit
    their username and email.
    """
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'blog/profile.html', {'form': form})
