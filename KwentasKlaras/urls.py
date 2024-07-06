# KwentasKlaras/urls.py
from django.contrib import admin
from django.urls import path, include
from KwentasApp.views import login_view

urlpatterns = [
    path('kwentasklarasmyadmin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('', include('KwentasApp.urls')),  # Include the app's URLs for the root path
]
