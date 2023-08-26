from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .serializers import GigSerializer
from account.utils import BaseResponse, abort
from gigs.models import Gigs

from django.http import QueryDict
# Create your views here.
class GigView(APIView):
    """
    view for handling users gigs
    POST - to post a gig of the authenticated user
    """
    permission_classes = (IsAuthenticated,)
    parser_classes = [MultiPartParser]
    serializer_class = GigSerializer
    

    def post(self, request):
        """
        Add a gig to your profile
        """
        print(request.data)

        # Create a mutable copy of request.data
        mutable_data = QueryDict('', mutable=True)
        mutable_data.update(request.data)
        
        # Assign the service_provider
        mutable_data['service_provider'] = request.user.id
        
        serializer = self.serializer_class(data=mutable_data, context={'request': request})
        
        try:
            
            serializer.is_valid(raise_exception=True)
            # print(serializer.data)
            
            serializer.save()
            base_response = BaseResponse(serializer.data, None, 'Gig created successfully')
            return Response(base_response.to_dict())
        except Exception as e:

            return abort(400, str(e))
    
    def get(self, request, gig_id):
        """
        Get a particular gig
        """
        
        gig = Gigs.objects.get(id=gig_id)
        serializer = self.serializer_class(gig, context={'request': request})
        base_response = BaseResponse(serializer.data, None, 'Gig gotten successfully')
        return Response(base_response.to_dict())
        
class AllGigsView(APIView):

    permission_classes = (IsAuthenticated,)
    parser_classes = [MultiPartParser]
    serializer_class = GigSerializer


    def get(self, request):
        """
        Get all gigs close to you if any. If there's no gig in your location it'll get all gigs generally
        """
        user = request.user

        if Gigs.objects.filter(gig_location=user.location).count() > 0:
            gig = Gigs.objects.filter(gig_location=user.location)
                
        else:
            gig = Gigs.objects.all()
            print(gig)

        serializer = self.serializer_class(gig, context={'request': request}, many=True)
        base_response = BaseResponse(serializer.data, None, 'Gig gotten successfully')
        return Response(base_response.to_dict())