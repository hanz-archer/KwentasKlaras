from django.urls import path
from . import views
from django.views.generic import RedirectView
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(pattern_name='login', permanent=False)),
    path('login/', views.login_view, name='login'),
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
    path('adddata/', views.adddata, name='adddata'),
    path('loginFailed/', views.loginFailed, name='loginFailed'),
    path('continuing', views.continuing, name='continuing'),
]