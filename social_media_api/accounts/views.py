from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

from .models import User
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer

#Register view
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

#Login view
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)

#Profile view
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

#FOLLOW view
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request, user_id):
    User = get_user_model()
    try:
        user_to_follow = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)

    if user_to_follow == request.user:
        return Response({'error': 'You cannot follow yourself'}, status=400)

    request.user.following.add(user_to_follow)
    return Response({'message': 'User followed'})

#UNFOLLOW view
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow_user(request, user_id):
    User = get_user_model()
    try:
        user_to_unfollow = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)

    request.user.following.remove(user_to_unfollow)
    return Response({'message': 'User unfollowed'})
