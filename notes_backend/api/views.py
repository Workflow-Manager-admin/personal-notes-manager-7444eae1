from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions, filters
from django.contrib.auth import logout
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from .models import Note
from .serializers import NoteSerializer, UserSerializer, RegisterSerializer, LoginSerializer

# Health endpoint (already exists)
@api_view(['GET'])
def health(request):
    """Health check endpoint for backend API."""
    return Response({"message": "Server is up!"})

# PUBLIC_INTERFACE
class RegisterView(APIView):
    """
    Endpoint for user registration.
    ---
    post:
      summary: Register a new user.
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/RegisterSerializer'
      responses:
        201:
          description: User registered successfully.
        400:
          description: Validation error.
    """
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(request_body=RegisterSerializer, responses={201: UserSerializer()})
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# PUBLIC_INTERFACE
class LoginView(APIView):
    """
    Endpoint for user login.
    ---
    post:
      summary: Log in a user (returns authentication token).
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/LoginSerializer'
      responses:
        200:
          description: Login successful, token returned.
        400:
          description: Invalid credentials.
    """
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key, "user": UserSerializer(user).data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# PUBLIC_INTERFACE
class LogoutView(APIView):
    """
    Endpoint for logging out user (delete auth token).
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        logout(request)
        return Response({"message": "Logged out successfully."}, status=status.HTTP_200_OK)

# PUBLIC_INTERFACE
class NoteViewSet(viewsets.ModelViewSet):
    """
    Viewset for managing notes CRUD and search/list. Authentication required.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NoteSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at', 'title']
    ordering = ['-updated_at']

    def get_queryset(self):
        # Only list/view notes belonging to the current user
        queryset = Note.objects.filter(owner=self.request.user)
        # Optional: extra filter by search or ordering via filter_backends
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# PUBLIC_INTERFACE
class CurrentUserView(APIView):
    """
    Returns the authenticated user's data.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)
