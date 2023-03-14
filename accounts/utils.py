from django.http import JsonResponse

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