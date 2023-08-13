from django.urls import path
from . import views


urlpatterns = [
    path('addgig/', views.GigView.as_view(), name='addgig'),
]

