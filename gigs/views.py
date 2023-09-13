from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from .serializers import GigSerializer, BookingSerializer, ClosingSerializer
from account.utils import BaseResponse, abort
from gigs.models import Gigs, Bookings, Reviews

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
    
    #TODO: fix up the cloudinary issues

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
        try:
            gig = Gigs.objects.get(id=gig_id)
            serializer = self.serializer_class(gig, context={'request': request})
            base_response = BaseResponse(serializer.data, None, 'Gig gotten successfully')
            return Response(base_response.to_dict())
        except Exception as e:
            return abort(400, str(e))

    #TODO: add a patch endpoint for editing a gig
        
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

class BookGig(APIView):
    permission_classes = (IsAuthenticated,)
    #permission_classes = []
    

    def post(self, request):
        """Endpoint to book a gig. It takes in the gig_id"""
        serializer = BookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)


        gig_id = serializer.validated_data['gig_id']

        try:
            gig = Gigs.objects.get(id=gig_id)
            print("hi")
        except Exception as e:
            print(str(e))
            abort(404, 'Gig does not exist')
        
        # restrict a user from booking their gig
        if gig.service_provider == request.user:
            return abort(403, "You cannot book your own gig")
        
        # create a booking
        gigBook = Bookings()
        gigBook.gig = gig
        gigBook.user = request.user
        gigBook.status = True
        gigBook.save()

        data = {
            "booking_id" : gigBook.id,
            "status": True

        }

        base_response = BaseResponse(data, None, 'Gig booked successfully')
        return Response(base_response.to_dict(), status=status.HTTP_201_CREATED)


#TODO: add the permissions for the two endpoints 
class CloseGig(APIView):
    permission_classes = (IsAuthenticated,)


    def post(self, request):
        """Endpoint to review and close a gig"""

        serializer = ClosingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        booking_id = serializer.validated_data['booking_id']
        review_chioce = serializer.validated_data['review_choice']
        rating = serializer.validated_data['rating']
        review_experience = serializer.validated_data['review_experience']

        try:
            booking = Bookings.objects.get(id=booking_id)
        except:
            return abort(404, "booking does not exist")
        booking.status = False
        booking.save()

            
        review = Reviews()
        review.gig = booking.gig
        review.reviewer = request.user
        review.rating = rating
        review.review_details = review_experience
        if review_chioce == "service_completed":
            review.review_choice = Reviews.CLOSE_GIG_CHOICE.SERVICE_COMPLETED
        elif review_chioce == "mind_change":
            review.review_choice = Reviews.CLOSE_GIG_CHOICE.MIND_CHANGE
        elif review_chioce == "service_provider_unavailable":
            review.review_choice = Reviews.CLOSE_GIG_CHOICE.SERVICE_PROVIDER_UNAVAILABLE
        else:
            return abort(404, "review choice not valid")
        
        review.save()

        data = {
            "booking_id": booking_id,
        }
        base_response = BaseResponse(data, None, 'Gig closed successfully')
        return Response(base_response.to_dict(), status=status.HTTP_201_CREATED)


   