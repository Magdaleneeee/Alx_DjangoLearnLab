# blog/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .forms import CustomUserCreationForm, UserUpdateForm, PostForm
from .models import Post


def index(request):
    """
    Home page: we simply show the list of posts here.
    """
    posts = Post.objects.all().order_by('-published_date')
    return render(request, 'blog/index.html', {'posts': posts})


def register(request):
    """
    User registration view.
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


# -----------------------------
# Class-based views for Post CRUD
# -----------------------------

class PostListView(ListView):
    """
    ListView to display all blog posts.
    Accessible to everyone.
    URL: /posts/
    """
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']


class PostDetailView(DetailView):
    """
    DetailView to display a single post.
    Accessible to everyone.
    URL: /posts/<pk>/
    """
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'


class PostCreateView(LoginRequiredMixin, CreateView):
    """
    CreateView to allow authenticated users to create posts.
    URL: /posts/new/
    The author is automatically set to the logged-in user.
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    UpdateView to allow authors to edit their own posts only.
    URL: /posts/<pk>/edit/
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        # Ensure the author remains the same user
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        """
        Only the author is allowed to update the post.
        """
        post = self.get_object()
        return post.author == self.request.user


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    DeleteView to allow authors to delete their own posts.
    URL: /posts/<pk>/delete/
    """
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = '/posts/'

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user
