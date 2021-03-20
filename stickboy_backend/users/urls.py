from django.urls import path
from users.views import UserRegistrationAPIView, UserLoginAPIView, UserTokenAPIView, UserListAPIView

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name="register"),
    path('login/', UserLoginAPIView.as_view(), name="login"),
    path('list/', UserListAPIView.as_view(), name="list"),
    path('tokens/<key>/', UserTokenAPIView.as_view(), name="token"),
]