from rest_framework import generics
from rest_framework.views import APIView
from .serializers import *
from .utils import response, abort
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from rest_framework import serializers, status
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.permissions import AllowAny
from django.conf import settings


User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """View for handling user registration.

    This view handles user registration and  returns a response with the serialized data of the newly created user.
    """
    authentication_classes = ()
    permission_classes = ()
    serializer_class = RegisterSerializer

class LoginView(TokenObtainPairView):
    """View for handling user authentication.

    This view is responsible for authenticating a user using the provided email and password. If the provided
    credentials are valid, the view returns a response with the user's authentication token. If the credentials are
    invalid, the view returns a 400 Bad Request response with an error message indicating that the provided
    credentials are incorrect.
    """
    serializer_class = LoginSerializer

class PasswordResetRequestView(APIView):
    authentication_classes = ()
    permission_classes = ()
    
    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'An account with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        token = RefreshToken.for_user(user).access_token
        send_password_reset_email(email, token)
        return Response({'success': 'An email with a reset link has been sent to your address.'}, status=status.HTTP_200_OK)

class PasswordResetConfirmView(APIView):
    authentication_classes = ()
    permission_classes = ()
    
    def post(self, request):
        token = request.data.get('token')
        password = request.data.get('password')
        try:
            user_id = AccessToken(token).payload['user_id']
            user = User.objects.get(id=user_id)
        except (User.DoesNotExist, KeyError):
            return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(password)
        user.save()
        return Response({'success': 'Password reset successful.'}, status=status.HTTP_200_OK)

class ProfileView(APIView):
    def get(self, request, user_id):
        try:
          obj = User.objects.get(id=user_id)
          serializer = UserSerializer(obj)
          return response(serializer.data)
        except User.DoesNotExist:
          return abort(404)

class SettingsView(APIView):
    """View for handling the settings of a user
    
    The view supports the following actions:
    - retrieve the current settings of a user (GET request)
    - update the settings of a user (POST request)
    """

    def get(self, request):
        """Retrieve the current settings of a user.

        Parameters:
        - request (django.http.request.HttpRequest): the HTTP request object

        Returns:
        - django.http.response.Response: a response containing the serialized user data

        Raises:
        - None
        """
        user = request.user
        serializer = SettingsSerializer(user)
        return response(serializer.data)

    def patch(self, request):
        """Update the settings of a user.

        Parameters:
        - request (django.http.request.HttpRequest): the HTTP request object

        Returns:
          A response containing the updated serialized user data

        Raises:
        - django.http.response.HttpResponseBadRequest: if the request data is not valid
        """
        user = request.user
        serializer = SettingsSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response(serializer.data)
        return abort(400, serializer.errors)