from django.urls import path
from . import views

urlpatterns = [
  path('sign-in/', views.sign_in),
  path('sign-up/', views.sign_up),
  path('profile/<int:pk>', views.user_detail),
]