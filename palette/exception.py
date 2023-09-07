from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework import status
from account.utils import abort  # Import your BaseResponse utility

def custom_exception_handler(exc, context):
   

    if isinstance(exc, AuthenticationFailed):
        custom_response_data = {
            'error': 'Token has expired'
        }
        return abort(401,  message="Token is invalid or expired")
        return Response(custom_response, status=status.HTTP_401_UNAUTHORIZED)

    return exception_handler(exc,context)
