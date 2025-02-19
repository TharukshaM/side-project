from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from api.models.user import CustomUser
from api.serializers.user import UserSerializer

class RegisterUserView(APIView):
    """User registration API (public)."""
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginUserView(APIView):
    """User login API (public)."""

    authentication_classes = []  # No authentication required
    permission_classes = []  # No permission required

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            # Create or get existing authentication token
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key, "user": {"id": user.id, "username": user.username, "email": user.email}}, status=status.HTTP_200_OK)

        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class UserProfileView(APIView):
    """User profile management API."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get the authenticated user's profile."""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        """Update the user's profile."""
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
