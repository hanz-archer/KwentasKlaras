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
from .forms import RegistrationForm





def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(reverse('homepage'))  # Use reverse to get the URL by name
        else:
            error = 'Invalid credentials. Please try again.'
            return render(request, 'KwentasApp/login.html', {'error': error})

    return render(request, 'KwentasApp/login.html')


def admin_view(request):
    return render(request, 'KwentasApp/admin')

@login_required
def base_view(request):
    logout(request)
    return redirect(reverse('login'))

@login_required
def reports_view(request):
    return render(request, 'KwentasApp/reports.html')

@login_required
def current_view(request):
    return render(request, 'KwentasApp/currentproject.html')

@never_cache
@login_required
def home_view(request):
    return render(request, 'KwentasApp/home.html')


def is_superuser(user):
    return user.is_authenticated and user.is_superuser




@user_passes_test(lambda u: u.is_superuser, login_url='login')
def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('<script>alert("Account Created."); window.location.href = "/login";</script>', status=200)
        else:
            # If form is invalid, render the registration form again with errors
            return HttpResponse('<script>alert("Account creation error, Please enter informations again."); window.location.href = "/register";</script>', status=200)
            return render(request, 'KwentasApp/register.html', {'form': form})
    else:
        form = RegistrationForm()

    return render(request, 'KwentasApp/register.html', {'form': form})



@login_required
def procurements(request):
    return render(request, 'KwentasApp/procurements.html')

@login_required
def ongoing(request):
    return render(request, 'KwentasApp/ongoing.html')


def logout_view(request):
    logout(request)
    return redirect(reverse('login'))


@login_required
def monitoring(request):
    return render(request,'KwentasApp/monitoring.html')

@login_required
def evaluation(request):
    return render(request,'KwentasApp/evaluation.html')


@login_required
def activities(request):
    return render(request,'KwentasApp/activities.html')


@login_required
def obligations(request):
    return render(request,'KwentasApp/obligations.html')


@login_required
def homepage(request):
    user_name = request.user.name  # Assuming 'name' is the correct attribute to access the user's name
    context = {'user_name': user_name}
    return render(request, 'KwentasApp/homepage.html', context)


@login_required
def finished(request):
    return render(request,'KwentasApp/finished.html')


@login_required
def ppa(request):
    return render(request, 'KwentasApp/ppa.html')

@login_required
def addbudget(request):
    return render(request, 'KwentasApp/addbudget.html')