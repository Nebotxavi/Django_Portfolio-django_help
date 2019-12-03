from django.urls import path
from .views import UserCreateAPIView, UserLoginAPIView

urlpatterns = [
    path('signin/', UserCreateAPIView.as_view(), name='signin'),
    path('login/', UserLoginAPIView.as_view(), name='login'),

]
