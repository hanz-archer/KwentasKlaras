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
    path('ongoing_projects/', ongoing_projects, name='ongoing_projects'),
    path('search/ongoing/', search_ongoing_projects, name='search_ongoing_projects'),
    path('search/continuing/', search_continuing_projects, name='search_continuing_projects'),
    path('continuing_add_obligation/', continuing_add_obligation, name='continuing_add_obligation'),
    path('ongoing_add_obligation/', ongoing_add_obligation, name='ongoing_add_obligation'),
    path('add_budget/', add_budget, name='add_budget'),
    path('ongoing_update_entry/', ongoing_update_entry, name='ongoing_update_entry'),
    path('continuing_update_entry/', continuing_update_entry, name='continuing_update_entry'),
    path('continuing_delete_entry/', continuing_delete_entry, name='continuing_delete_entry'),
    path('ongoing_delete_entry/', ongoing_delete_entry, name='ongoing_delete_entry'),
    path('base/', views.base_view, name='base'),
    path('register/', views.registration_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('reports/', reports_view, name='reports'),
    path('procurements/', views.procurements, name='procurements'),
    path('ongoing/', views.ongoing, name='ongoing'),
    path('monitoring/', views.monitoring, name='monitoring'),
    path('evaluation/', views.evaluation, name='evaluation'),
    path('activities/', views.activities, name='activities'),
    path('obligations/', views.obligations, name='obligations'),
    path('finished/', views.finished, name='finished'),
    path('currentproject/', views.current_view, name='currentprojects'),
    path('homepage/', views.homepage, name='homepage'),
    path('adddata/', adddata, name='adddata'),
    path('ppa/', views.ppa, name='ppa'),
    path('addbudget/', views.addbudget, name='addbudget'),
    path('unset_just_logged_in/', unset_just_logged_in, name='unset_just_logged_in'),
    path('forgot-password/', views.forgotpassword, name='forgot-password'),
    path('send-verification-code/', views.send_verification_code, name='send_verification_code'),
    path('verify-and-change-password/', views.verify_and_change_password, name='verify_and_change_password'),
]
