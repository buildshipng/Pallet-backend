from django.shortcuts import render
from .models import Notifications
from rest_framework.generics import ListAPIView, DestroyAPIView
from  rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from account.utils import BaseResponse, abort
from .serializers import *


# Create your views here.

class ViewNotification(ListAPIView):
    permission_classes = (IsAuthenticated)
    parser_classes = (MultiPartParser)
    queryset = Notifications.objects.all()
    serializer_class = NotificationSerializer
    
    def get_queryset(self):
        return self.queryset.filter(user_id=self.request.user.id)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        data = {
            "count": queryset.count(),
            "result": serializer.data,
        }
        
        base_response = BaseResponse(data, None, 'Notifications Listed')
        return Response(base_response.to_dict(), status=status.HTTP_200_CREATED)

    