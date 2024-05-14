from django.urls import path
from . import views
from django.views.generic import RedirectView
from django.contrib import admin
from .projects import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(pattern_name='login', permanent=False)),
        path('login/', views.login_view, name='login'),

    path('create_entry/', create_entry, name='create_entry'),

path('continuing_projects', continuing_projects, name='continuing_projects'),
    path('ongoing_projects', ongoing_projects, name='ongoing_projects'),
   path('search/ongoing/', search_ongoing_projects, name='search_ongoing_projects'),
   path('search/ongoing/', search_ongoing_projects, name='search_ongoing_projects'),
 path('search/continuing/', search_continuing_projects, name='search_continuing_projects'),
   path('add_obligation', add_obligation, name='add_obligation'),
 path('add_budget/', add_budget, name='add_budget'),


    path('base/', views.base_view, name='base'),
    path('register/', views.registration_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home_view, name='home'),
    path('reports/', views.reports_view, name='reports'),
    path('procurements/', views.procurements, name='procurements'),
    path('ongoing/', views.ongoing, name='ongoing'),
    path('monitoring/', views.monitoring, name='monitoring'),                        
    path('evaluation/', views.evaluation, name='evaluation'),                                                                                                                                    
    path('evaluation/', views.evaluation, name='evaluation'),
    path('activities/', views.activities, name='activities'),     
    path('obligations/', views.obligations, name='obligations'),  
    path('disbursements/', views.disbursements, name='disbursements'),  
    path('finished/', views.finished, name='finished'), 
    path('currentproject', views.current_view, name='currentprojects'),
    path('homepage/', views.homepage, name='homepage'),
    path('adddata/', adddata, name='adddata'),
    path('loginFailed/', views.loginFailed, name='loginFailed'),
  
    path('ppa', views.ppa, name='ppa'),
    path('addbudget', views.addbudget, name='addbudget'),
]