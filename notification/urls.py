from django.urls import path
from .views import ViewNotification

urlpatterns = [
    path('notifications/', ViewNotification.as_view(), name='notifications-list'),
]
