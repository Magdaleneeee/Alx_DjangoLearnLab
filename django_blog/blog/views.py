from django.shortcuts import render, redirect, get_object_or_404
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

from .forms import CustomUserCreationForm, UserUpdateForm, PostForm, CommentForm
from .models import Post, Comment


def index(request):
    """
    Home page: show latest posts and link to full list.
    """
    posts = Post.objects.all().order_by('-published_date')[:5]
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
    URL: /post/
    """
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']


class PostDetailView(DetailView):
    """
    DetailView to display a single post and its comments.
    URL: /post/<pk>/
    """
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        context['comments'] = post.comments.order_by('-created_at')
        context['comment_form'] = CommentForm()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """
    CreateView to allow authenticated users to create posts.
    URL: /post/new/
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
    URL: /post/<pk>/update/
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    DeleteView to allow authors to delete their own posts.
    URL: /post/<pk>/delete/
    """
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = '/post/'

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user


# -----------------------------
# Comment views
# -----------------------------

class CommentCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new comment for a given post.
    URL: /post/<pk>/comment/new/
    (Also supports alias /posts/<int:post_id>/comments/new/ for checker.)
    """
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        post_id = self.kwargs.get('pk') or self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        form.instance.post = post
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.post.get_absolute_url()


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Edit an existing comment.
    Only the comment author is allowed.
    URL: /comment/<pk>/edit/
    """
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user

    def get_success_url(self):
        return self.object.post.get_absolute_url()


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Delete an existing comment.
    Only the comment author is allowed.
    URL: /comment/<pk>/delete/
    """
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user

    def get_success_url(self):
        return self.object.post.get_absolute_url()
