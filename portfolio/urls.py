from django.urls import path
from . import views


urlpatterns = [
    path('addportfolio/', views.PortfolioView.as_view(), name='addportfolio'),
    path('business/', views.BusinessView.as_view(), name='business'),
]
