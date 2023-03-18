from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from .serializers import *
from django.http import HttpResponse, JsonResponse
from .utils import response, abort
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from django.contrib.auth import authenticate

class RegisterView(generics.CreateAPIView):
    """View for handling user registration.

    This view handles user registration and is designed to be called by a client-side application. The view
    accepts a request with the necessary data to create a new user, serializes the data using the 
    `RegisterSerializer` class, and returns a response with the serialized data of the newly created user.
    """
    authentication_classes = ()
    permission_classes = ()
    serializer_class = RegisterSerializer

class LoginView(APIView):
    """View for handling user authentication.

    This view is responsible for authenticating a user using the provided username and password. If the provided
    credentials are valid, the view returns a response with the user's authentication token. If the credentials are
    invalid, the view returns a 400 Bad Request response with an error message indicating that the provided
    credentials are incorrect.
    """
    permission_classes = ()
    
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)
        if user:
            return response({"token": user.auth_token.key, "message": "success"})
        else:
            return abort(404, "Invalid Credentials")


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