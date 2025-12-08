from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    PostByTagListView,
    CommentCreateView,
    CommentUpdateView,
)


urlpatterns = [
    # Home
    path('', views.index, name='blog-index'),
    path('tags/<slug:tag_slug>/', PostByTagListView.as_view(), name='posts_by_tag'),

    # Auth
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='blog/login.html'),
        name='login'
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(template_name='blog/logout.html'),
        name='logout'
    ),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),

    # Post CRUD
    path('post/', views.PostListView.as_view(), name='post-list'),
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),

    # Comment URLs must match EXACT checker pattern
    path("post/<int:pk>/comments/new/", CommentCreateView.as_view(), name="comment_create"),
    path("comment/<int:pk>/update/", CommentUpdateView.as_view(), name="comment_update"),

    # Tag and search
    path('tags/<str:tag_name>/', views.TagPostListView.as_view(), name='tag-posts'),
    path('search/', views.SearchResultsView.as_view(), name='post-search'),
]
