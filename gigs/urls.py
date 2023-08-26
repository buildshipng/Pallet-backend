from django.urls import path
from . import views


urlpatterns = [
    path('addgig/', views.GigView.as_view(), name='addgig'),
    path('gig/<int:gig_id>/', views.GigView.as_view(), name='getgig'),
    path('all/', views.AllGigsView.as_view(), name='getallgigs')
]

