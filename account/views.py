from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.views import APIView
from .serializers import *
from .utils import response, abort, TokenGenerator, BaseResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from rest_framework import serializers, status
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken, OutstandingToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny
from django.conf import settings
from .models import Tokens
import time
from django.db.models import Q
from django.core.mail import send_mail
from rest_framework.parsers import MultiPartParser



User = get_user_model()
toke = TokenGenerator()
passtoke = TokenGenerator()

class RegisterView(generics.CreateAPIView):
    """View for handling user registration.
    This view handles user registration and  returns a response with the serialized data of the newly created user.
    """

    authentication_classes = ()
    permission_classes = ()
    serializer_class = RegisterSerializer
    def create(self, request, *args, **kwargs):
        exception = None
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()

            token = str(random.randint(1000, 9999))
            # OTP token
            new_token = Tokens()
            new_token.email = user.email
            new_token.action = 'register'
            new_token.token = token
            new_token.exp_date = time.time() + 300
            new_token.save()

            print(token)
            # send_mail(
            #     "Test",
            #     "This is a test message with token: \n" + token,
            #     "buildshipng@gmail.com",
            #     [user.email],
            #     fail_silently=False,
            # )
            # Customize the response data
            response_data = {
                'full_name': user.full_name,
                'email': user.email,
                'token': token
                # Add any other fields you want to include in the response
            }
            base_response = BaseResponse(data=response_data, exception=exception, message="User Created Successful")
            return Response(base_response.to_dict())
        except Exception as e:
            return abort(400, "User registration failed")

            
        return Response(response_data, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    """View for handling user authentication.
    This view is responsible for authenticating a user using the provided email and password. If the provided
    credentials are valid, the view returns a response with the user's authentication token. If the credentials are
    invalid, the view returns a 400 Bad Request response with an error message indicating that the provided
    credentials are incorrect.
    """
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):

        try:

            serializer = self.get_serializer(data=request.data)
            # serializer.is_valid(raise_exception=True)

            try:
                email = serializer.initial_data['email']
                password = serializer.initial_data['password']
            except:
                raise AuthenticationFailed('Email and password required')

            try:
                print(email)
                user = User.objects.get(email=email)
                if not user.check_password(password):
                    raise AuthenticationFailed('Invalid email or password.')

                if not user.is_active:
                    raise AuthenticationFailed('Your account is not active.')
            except User.DoesNotExist:
                raise AuthenticationFailed('Invalid email or password.')

            serializer = SettingsSerializer(user)
            response =  super().post(request, *args, **kwargs)
            responseData = {
                "Authorization": response.data,
                "user_data": serializer.data
            }
            response.data = BaseResponse(responseData, None, 'Login successful').to_dict()
            return Response(response.data, status=status.HTTP_200_OK)
        except AuthenticationFailed as e:
            return abort(401, (e.detail)['detail'])
            # return Response({'error': e.detail}, status=status.HTTP_401_UNAUTHORIZED)
        # return Response(serializer.validated_data, status=status.HTTP_200_OK)

class PasswordResetRequestView(APIView):
    """
    View to request for an otp to reset password
    """
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
        

            
            token = str(random.randint(1000, 9999))
            # OTP token
            new_token = Tokens()
            new_token.email = email
            new_token.action = 'resetpassword'
            new_token.token = token
            new_token.exp_date = time.time() + 300
            new_token.save()

            
            data = {
                'Token': token
            }
            base_response = BaseResponse(data, None, 'Reset OTP send to email')
            return Response(base_response.to_dict(), status=status.HTTP_201_CREATED)
            return Response({'Token': token, 'message': "success"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            # return Response({'error': 'An account with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)
            return abort(404, 'An account with this email does not exist.')
        # token = RefreshToken.for_user(user).access_token
        # send_password_reset_email(email, token)
        # return Response({'success': 'An email with a reset link has been sent to your address.'}, status=status.HTTP_200_OK)

class PasswordResetConfirmView(APIView):
    """
    This view is used to verify a reset password token
    """
    authentication_classes = ()
    permission_classes = ()

    
    def post(self, request):
        serializer = PassVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        verification_token = serializer.validated_data['verification_token']
        

        try:
            user = User.objects.get(email=email)
            #verify the token that was passed
            token = Tokens.objects.filter(Q(email=email) & Q(action='resetpassword')).order_by('-created_at')[:1].first()
            print(token)
            result = check_password(verification_token, token.token)
            if result == True and token.exp_date >= time.time():
                token.date_used = datetime.now()
                token.confirmed = True
                user.save()
                token.save()

                base_response = BaseResponse(None, None, 'Token verified successfully.')
                return Response(base_response.to_dict(), status=status.HTTP_200_OK)
                return Response({'success': 'Password reset successful.'}, status=status.HTTP_200_OK)
            elif result and token.exp_date < time.time():
                return abort(401, 'Expired  token')

            else:
                raise User.DoesNotExist

        except User.DoesNotExist:
            return abort(401, 'Invalid  token')


class PasswordResetView(APIView):
    """
    This view is used to reset a password
    """
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        serializer = PassResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            user = User.objects.get(email=email)
            #verify the token that was passed
            token = Tokens.objects.filter(Q(email=email) & Q(action='resetpassword')).order_by('-created_at')[:1].first()
            print(token)
            
            if token.confirmed:
                user.set_password(password)
                user.save()
                base_response = BaseResponse(None, None, 'Password reset successful.')
                return Response(base_response.to_dict(), status=status.HTTP_200_OK)
                return Response({'success': 'Password reset successful.'}, status=status.HTTP_200_OK)
            else:
                raise User.DoesNotExist

        except User.DoesNotExist:
            return abort(401, 'Invalid  token')

class ProfileView(APIView):
    """
    View to get the details of a user 
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, user_id):
        try:
          obj = User.objects.get(id=user_id)
          serializer = UserSerializer(obj)
          responseData = BaseResponse(serializer.data, None, 'User Profile').to_dict()
          return response(responseData)
        except User.DoesNotExist:
          return abort(404, 'User Does not exist')

# This view is actually the profile view
class SettingsView(APIView):
    """View for handling the settings of a user

    The view supports the following actions:
    - retrieve the current settings of a user (GET request)
    - update the settings of a user (POST request)
    """
    permission_classes = (IsAuthenticated,)
    parser_classes = [MultiPartParser]

    def get(self, request):
        """Retrieve the current details of a user.
        Parameters:
        - request (django.http.request.HttpRequest): the HTTP request object
        Returns:
        - django.http.response.Response: a response containing the serialized user data
        Raises:
        - None
        """
        exception = None
        try:
            user = request.user
            print(user)
            serializer = SettingsSerializer(user)
            
        except Exception as e:
            exception = e
        base_response = BaseResponse(data=serializer.data, exception=exception, message="User Data fetch Successful")
        return Response(base_response.to_dict(), status=status.HTTP_200_OK)
        

    def patch(self, request):
        """Update the details of a user.
        Parameters:
        - request (django.http.request.HttpRequest): the HTTP request object
        Returns:
          A response containing the updated serialized user data
        Raises:
        - django.http.response.HttpResponseBadRequest: if the request data is not valid
        """
        
        exception = None
        user = request.user
        serializer = SettingsSerializer(user, data=request.data)
        try:
            #avatar_file = request.FILES.get('avatar')
            #if avatar_file:
                # Save the avatar file to the user's avatar field
                # request.user.avatar = avatar_file
                # request.user.save()
            serializer.is_valid(raise_exception=True)
            serializer.save()
            # return response(serializer.data)
            base_response = BaseResponse(data=serializer.data, exception=exception, message="User Data Updated Successfully")
            return Response(base_response.to_dict(), status=status.HTTP_200_OK)
        except Exception as e:
            exception = e
            print(exception)
        

        return abort(400, serializer.errors)

    

class VerificationView(APIView):
    """
    This view verifies cteating account with otp

    POST - takes the otp and the email to verify
    """
    permission_classes = ()

    def post(self, request):
        serializer = VerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        verification_token = serializer.validated_data['verification_token']

        try:
            user = User.objects.get(email=email)
            #verify the token that was passed
            # token = Tokens.objects.get(email=email)
            token = Tokens.objects.filter(Q(email=email) & Q(action='register')).order_by('-created_at')[:1].first()

            result = check_password(verification_token, token.token)
            if result == True and token.exp_date >= time.time():
                token.date_used = datetime.now()
                user.is_active = True
                user.save()
                token.save()

                exception = None
                try:
                    
                    print(user)
                    userserializer = SettingsSerializer(user)
                except Exception as e:
                    exception = e
                
                base_response = BaseResponse(data=userserializer.data, exception=exception, message='User successfully verified')
                return Response(base_response.to_dict(), status=status.HTTP_200_OK)
                
            elif result and token.exp_date < time.time():
                return abort(401, 'Token has expired')
            else:
                raise User.DoesNotExist

        except User.DoesNotExist:
            return abort(401, 'Invalid verification token')


class LogoutView(APIView):
    """
    View to logout a user
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
           
            token = RefreshToken(refresh_token)
            token.blacklist()
            base_response = BaseResponse(None, None, 'Successfully logged out.')
            return Response(base_response.to_dict(), status=status.HTTP_200_OK)
        except Exception as e:
            print(type(str(e)))
            return abort(400, str(e))


class RegisterRefreshView(APIView):
    """
    This view generates a new otp for signing up
    """
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        try:
            email = request.data.get('email')

            token = str(random.randint(1000, 9999))
            # OTP token
            new_token = Tokens()
            new_token.email = email
            new_token.action = 'register'
            new_token.token = token
            new_token.exp_date = time.time() + 300
            new_token.save()

            # send_mail(
            #     "Test",
            #     "This is a test message with token: \n" + token,
            #     "buildshipng@gmail.com",
            #     [email],
            #     fail_silently=False,
            # )
            data = {
                'token': token,
                'email': email
            }
            base_response = BaseResponse(data, None, 'Register OTP send to email')
            return Response(base_response.to_dict(), status=status.HTTP_205_RESET_CONTENT)
        except:
            return abort(400, 'An error occured. Please Try again')

        # token = RefreshToken.for_user(user).access_token
        # send_password_reset_email(email, token)
        # return Response({'success': 'An email with a reset link has been sent to your address.'}, status=status.HTTP_200_OK)
