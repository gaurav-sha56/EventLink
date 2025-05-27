from django.contrib import admin
from django.urls import path
from Home import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('logout', views.logoutUser, name='logout'),
    path('home/', views.home, name='home'),
    path('student_login', views.student_login, name='student_login'),
    path('college_login', views.college_login, name='college_login'),
    path('student_register', views.student_register, name='student_register'),
    path('college_register', views.college_register, name='college_register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile', views.profile, name='profile'),
    path('find_teammates', views.find_teammates, name='find_teammates'),
    path('create_team', views.create_team, name='create_team'),
    path('complete-profile/', views.complete_profile, name='complete_profile'),
    path('teams/request/<int:team_id>/', views.send_request, name='send_request'),
    path('teams', views.send_request, name='teams'),
    path('teams/requests/', views.team_requests, name='team_requests'),
    path('teams/requests/<int:request_id>/<str:action>/', views.update_request, name='update_request'),
    path('teams/requests/cancel/<int:request_id>/', views.cancel_request, name='cancel_request'),
    path('event_detail/<int:event_id>/', views.event_detail, name='event_detail'),
    path('events/<int:event_id>/register/', views.register_team, name='register_team'),
    path('events/<int:event_id>/register/find-teammates', views.find_teammates, name='find_teammates'),
    path('requests/<int:request_id>/accept/', views.accept_request, name='accept'),
    path('requests/<int:request_id>/reject/', views.reject_request, name='reject'),


]
