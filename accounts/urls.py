from django.urls import path
from accounts import views

app_name = "accounts"

urlpatterns = [
    path('login/', views.LoginView.as_view()),
    path('register/', views.RegisterView.as_view()),
    path('settings/', views.SettingsView.as_view()),
    path('<int:user_id>/', views.ProfileView.as_view()),
]