from django.urls import path
from .views import RegisterUserView, LoginUserView, UserProfileView

urlpatterns = [
    path('auth/register/', RegisterUserView.as_view(), name='register'),
    path('auth/login/', LoginUserView.as_view(), name='login'),
    path('auth/profile/', UserProfileView.as_view(), name='profile'),
]
