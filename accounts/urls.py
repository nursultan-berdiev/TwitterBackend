from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.UserRegisterAPIView.as_view()),
    path('users/', views.UserListAPIView.as_view())
]