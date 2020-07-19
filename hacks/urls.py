from django.urls import path
from . import views

urlpatterns = [
  path('', views.hacks_list, name='hacks-list-api'),
  path('check/<int:pk>', views.hacks_check, name='hacks-check-api'),
  path('<int:pk>', views.hacks_detail, name='hacks-detail-api'),
  path('team/', views.team_list, name='team-list-api'),
  path('team/<int:pk>', views.team_detail, name='team-detail-api'),
  path('apply/', views.application_list, name='application-list-api'),
  path('apply/<int:pk>', views.application_detail, name='application-detail-api'),
  path('<int:pk>/team-build/', views.team_build, name='team_build-api'),
  path('<int:pk>/ideation/', views.ideation, name='ideation-api'),
  path('<int:pk>/submit/', views.submit, name='submit-api'),
]