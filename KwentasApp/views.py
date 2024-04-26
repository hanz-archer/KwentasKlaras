from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(reverse('home'))  # Use reverse to get the URL by name
        else:
            error = 'Invalid credentials. Please try again.'
            return render(request, 'KwentasApp/login.html', {'error': error})

    return render(request, 'KwentasApp/login.html')

@login_required
def base_view(request):
    logout(request)
    return redirect(reverse('login'))

def reports_view(request):
    return render(request, 'KwentasApp/reports.html')


def current_view(request):
    return render(request, 'KwentasApp/currentproject.html')

@never_cache
@login_required
def home_view(request):
    return render(request, 'KwentasApp/home.html')


def is_superuser(user):
    return user.is_authenticated and user.is_superuser

@user_passes_test(is_superuser, login_url='login')
def registration_view(request):

    if not is_superuser(request.user):
        messages.warning(request, 'Only superusers can access the registration page.')
        return redirect('login')
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully. You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Error creating account. Please check the form data.')
    else:
        form = RegistrationForm()

    return render(request, 'KwentasApp/register.html', {'form': form})

def procurements(request):
    return render(request, 'KwentasApp/procurements.html')


def ongoing(request):
    return render(request, 'KwentasApp/ongoing.html')


def logout_view(request):
    logout(request)
    return redirect(reverse('login'))



def monitoring(request):
    return render(request,'KwentasApp/monitoring.html')


def evaluation(request):
    return render(request,'KwentasApp/evaluation.html')

def activities(request):
    return render(request,'KwentasApp/activities.html')

def obligations(request):
    return render(request,'KwentasApp/obligations.html')


def disbursements(request):
    return render(request,'KwentasApp/disbursements.html')


def finished(request):
    return render(request,'KwentasApp/finished.html')