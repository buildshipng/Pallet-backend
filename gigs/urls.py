from django.urls import path
from . import views


urlpatterns = [
    path('addgig/', views.GigView.as_view(), name='addgig'),
    path('getgig/<uuid:gig_id>/', views.GigView.as_view(), name='getgig'),
    path('all/', views.AllGigsView.as_view(), name='getallgigs'),
    path('bookgig/', views.BookGig.as_view(), name='bookgig'),
    path('closegig/', views.CloseGig.as_view(), name='closegig'),
]

