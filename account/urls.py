from django.urls import path
from accounts import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = "accounts"

urlpatterns = [
    path('login/', TokenObtainPairView.as_view()),
    path('login/refresh/', TokenRefreshView.as_view(), name='login_refresh'),
    path('register/', views.RegisterView.as_view()),
    path('reset/', views.PasswordResetRequestView.as_view(), name='password_reset'),
    path('reset/confirm/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('settings/', views.SettingsView.as_view()),
    path('<int:user_id>/', views.ProfileView.as_view()),
]