from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import PortfolioSerializer, BusinessSerializer, Portfolio
from account.utils import BaseResponse, abort
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser

from django.http import QueryDict

# Create your views here.
class PortfolioView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = [MultiPartParser]
    serializer_class = PortfolioSerializer

    def post(self, request):
        print(request.user.id)
        
        # Create a mutable copy of request.data
        mutable_data = QueryDict('', mutable=True)
        mutable_data.update(request.data)
        
        # Assign the service_provider
        mutable_data['service_provider'] = request.user.id
        
        serializer = self.serializer_class(data=mutable_data, context={'request': request})
        
        print(request.data)
        try:
            
            serializer.is_valid(raise_exception=True)
            print(serializer.validated_data)
            serializer.save()
            base_response = BaseResponse(serializer.data, None, 'Portfolio created successfully')
            return Response(base_response.to_dict())
        except Exception as e:
            return abort(400, str(e))

class BusinessView(APIView):
    permission_classes = (IsAuthenticated,)
    

    def post(self, request):
        print(request.user.id)
        request.data['service_provider'] = request.user.id
        serializer = BusinessSerializer(data=request.data, context={'request': request})
        try:
            serializer.is_valid(raise_exception=True)
            # print(serializer.data)
            print(serializer.validated_data)
            serializer.save()
            base_response = BaseResponse(serializer.data, None, 'Business created successfully')
            return Response(base_response.to_dict())
        except:

            return abort(400, serializer.errors)