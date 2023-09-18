from django.urls import path
from .views import ViewNotification

urlpatterns = [
    path('all-message/', ViewNotification.as_view(), name='notifications-list'),
]
