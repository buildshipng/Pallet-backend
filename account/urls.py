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

    path('reset/request/', views.PasswordResetRequestView.as_view(), name='password_request'),
    path('reset/confirm/', views.PasswordResetConfirmView.as_view(), name='password_confirm'),
    path('reset/', views.PasswordResetView.as_view(), name='password_reset'),

    path('settings/', views.SettingsView.as_view()),
    path('<int:user_id>/', views.ProfileView.as_view()),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    
    

    
]