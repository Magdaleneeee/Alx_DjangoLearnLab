from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Notification


class NotificationListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(
            recipient=self.request.user
        ).order_by('-timestamp')
