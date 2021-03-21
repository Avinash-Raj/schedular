from django.urls import path
from users.views import UserRegistrationAPIView, UserLoginAPIView, UserTokenAPIView, UserListAPIView, ChangePasswordView

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name="register"),
    path('login/', UserLoginAPIView.as_view(), name="login"),
    path('list/', UserListAPIView.as_view(), name="list"),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('tokens/<key>/', UserTokenAPIView.as_view(), name="token"),
]