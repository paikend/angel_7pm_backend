from django.urls import path
from . import views

urlpatterns = [
  path('', views.hacks_list, name='hacks-list-api'),
  path('<int:pk>', views.hacks_detail, name='hacks-detail-api'),
  path('team/', views.team_list, name='team-list-api'),
  path('team/<int:pk>', views.team_detail, name='team-detail-api'),
  path('apply/', views.application_list, name='application-list-api'),
  path('team-build/<int:pk>', views.team_build, name='team_build-api'),
  path('ideation/<int:pk>', views.ideation, name='ideation-api'),
  path('submit/<int:pk>', views.submit, name='submit-api'),
]