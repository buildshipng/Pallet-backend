from django.http import JsonResponse
from django.core.mail import send_mail

def abort(code, message=None):
  '''
  Returns an endpoint with an error code and message
  '''
  messages = {
    404: 'The requested resource cannot be found.',
    403: 'Not allowed.',
    422: 'The request cannot be processed.',
    400: 'Bad Request.',
    }
  message = message or messages.get(code, '')
  data = {
    'success': False,
    'error': code,
    'message': message
  }
  return JsonResponse(data, json_dumps_params={'indent': 2}, status=code)

def response(data, status=None):
  '''
  Returns an endpoint with data
  '''
  status = status or 200
  return JsonResponse(data, json_dumps_params={'indent': 2}, safe=False, status=status)

def send_password_reset_email(email, reset_token):
    """
    Sends a password reset email to the user with the given email address,
    containing a link to the password reset confirmation page with the
    provided reset token.
    """
    subject = 'Password Reset Request'
    recipient = [email]
    message = f'Hi {user.full_name},\n\nPlease click on the following link to reset your password: {settings.FRONTEND_URL}/reset/confirm/?token={token} \n\nThanks,\nPalette Team'
    send_mail(
      subject,
      message,
      settings.EMAIL_HOST_USER,
      recipient,
      fail_silently=True,
    )
    
    print(message)