from django.urls import path
from . import views
from django.views.generic import RedirectView
from django.contrib import admin
from .projects import *
from .views import login_view, unset_just_logged_in

print("KwentasApp.urls module loaded")  # Debugging print

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='login', permanent=False)),
    path('login/', views.login_view, name='login'),
    path('create_entry/', create_entry, name='create_entry'),
    path('continuing_projects/', continuing_projects, name='continuing_projects'),
    path('current_projects/', current_projects, name='current_projects'),
    path('search/current/', search_current_projects, name='search_current_projects'),
    path('search/continuing/', search_continuing_projects, name='search_continuing_projects'),
   path('add_obligation/<str:project_type>/', add_obligation, name='add_obligation'),
    path('add_budget/', add_budget, name='add_budget'),
   path('update_entry/<str:project_type>/', update_entry, name='update_entry'),
    path('continuing_delete_entry/', continuing_delete_entry, name='continuing_delete_entry'),
    path('current_delete_entry/', current_delete_entry, name='current_delete_entry'),
    path('base/', views.base_view, name='base'),
    path('register/', views.registration_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('reports/', reports_view, name='reports'),
   
    
    path('homepage/', views.homepage, name='homepage'),
  
   
    path('unset_just_logged_in/', unset_just_logged_in, name='unset_just_logged_in'),
    path('forgot-password/', views.forgotpassword, name='forgot-password'),
    path('send-verification-code/', views.send_verification_code, name='send_verification_code'),
    path('verify-and-change-password/', views.verify_and_change_password, name='verify_and_change_password'),



path(' samplechart/',  samplechart, name='samplechart'),
  path('api/get_monthly_expenses/', get_monthly_expenses_view, name='get_monthly_expenses'),
        path('all-projects/', all_projects, name='all_projects'),
       
          path('download_word/<str:project_code>/', download_word, name='download_word'),
]
