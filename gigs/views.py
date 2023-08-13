from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import GigSerializer
from account.utils import BaseResponse, abort
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser


# Create your views here.
class GigView(APIView):
    """
    view for handling users gigs
    POST - to post a gig of the authenticated user
    """
    permission_classes = (IsAuthenticated,)
    parser_classes = [MultiPartParser]

    

    def post(self, request):
        print(request.user.id)
        request.data['service_provider'] = request.user.id
        serializer = GigSerializer(data=request.data, context={'request': request})
        try:
            
            serializer.is_valid(raise_exception=True)
            # print(serializer.data)
            
            serializer.save()
            base_response = BaseResponse(serializer.data, None, 'Gig created successfully')
            return Response(base_response.to_dict())
        except Exception as e:

            return abort(400, str(e))
