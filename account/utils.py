from django.http import JsonResponse
from django.core.mail import send_mail
from django_otp.oath import TOTP
from django_otp.util import random_hex
import time
import random
import time

class TokenGenerator:
  def __init__(self, token_validity_period=100):
    self.generated_tokens = {}
    self.token_validity_period = token_validity_period

  def generate_token(self):
    # Generate a new unique token with an expiration timestamp
    while True:
        token = str(random.randint(1000, 9999))
        expiration_time = time.time() + self.token_validity_period
        if token not in self.generated_tokens or self.generated_tokens[token] < time.time():
            self.generated_tokens[token] = expiration_time
            return token

  def verify_token(self, token):
    # Verify the token and check for expiration
    if token in self.generated_tokens:
        if self.generated_tokens[token] >= time.time():
            return True
        else:
            del self.generated_tokens[token]
    return False


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


#token
class TOTPVerification:
    
  def __init__(self):
    # secret key that will be used to generate a token,
    # User can provide a custom value to the key.
    self.key = bytes(random_hex(20), 'utf-8')
    # counter with which last token was verified.
    # Next token must be generated at a higher counter value.
    self.last_verified_counter = -1
    # this value will return True, if a token has been successfully
    # verified.
    self.verified = False
    # number of digits in a token. Default is 6
    self.number_of_digits = 4
    # validity period of a token. Default is 30 second.
    self.token_validity_period = 150
    self.totp = None

  def totp_obj(self):
    # create a TOTP object
    totp = TOTP(key=self.key,
                step=self.token_validity_period,
                digits=self.number_of_digits)
    # the current time will be used to generate a counter
    totp.time = time.time()
    return totp

  def generate_token(self):
    # get the TOTP object and use that to create token
    totp = self.totp_obj()
    # token can be obtained with `totp.token()`
    token = str(totp.token()).zfill(self.number_of_digits)
    return token


  def verify_token(self, token, tolerance=0):
    try:
        # convert the input token to integer
        token = int(token)
    except ValueError:
        # return False, if token could not be converted to an integer
        self.verified = False
    else:
        totp = self.totp_obj()
        # check if the current counter value is higher than the value of
        # last verified counter and check if entered token is correct by
        # calling totp.verify_token()
        if ((totp.t() > self.last_verified_counter) and
                (totp.verify(token, tolerance=tolerance))):
            # if the condition is true, set the last verified counter value
            # to current counter value, and return True
            self.last_verified_counter = totp.t()
            self.verified = True
        else:
            # if the token entered was invalid or if the counter value
            # was less than last verified counter, then return False
            self.verified = False
    return self.verified