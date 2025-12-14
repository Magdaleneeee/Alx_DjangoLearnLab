from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    PostViewSet,
    CommentViewSet,
    FeedView,
    like_post,
    unlike_post
)

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = router.urls

urlpatterns += [
    path('feed/', FeedView.as_view()),
    path('posts/<int:pk>/like/', like_post),
    path('posts/<int:pk>/unlike/', unlike_post),
]
