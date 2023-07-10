from django.urls import path
from account import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = "account"

urlpatterns = [
    path('login/', views.LoginView.as_view()),
    path('login/refresh/', TokenRefreshView.as_view(), name='login_refresh'),
    path('register/', views.RegisterView.as_view()),
    path('resendtoken/', views.RegisterRefreshView.as_view()),
    path('verify/', views.VerificationView.as_view(), name='verify'),
    path('reset/', views.PasswordResetRequestView.as_view(), name='password_reset'),
    path('reset/confirm/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('settings/', views.SettingsView.as_view()),
    path('<int:user_id>/', views.ProfileView.as_view()),
    path('gigs/', views.GigView.as_view(), name='gigs'),
    path('portfolio/', views.PortfolioView.as_view(), name='portfolio'),
    path('business/', views.BusinessView.as_view(), name='business'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    
]