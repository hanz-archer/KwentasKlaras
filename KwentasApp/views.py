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
from django.http import HttpResponseRedirect
from django.http import JsonResponse



print("KwentasApp.views module loaded")  # Debugging print

#this def ensures the Sweet Alert in Homepage just shows after loggin in only
def unset_just_logged_in(request):
    if 'just_logged_in' in request.session:
        del request.session['just_logged_in']
    return JsonResponse({'status': 'success'})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Set the session flag after successful login
            request.session['just_logged_in'] = True
            return redirect(reverse('homepage'))  # Redirect to homepage
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
def current_view(request):
    return render(request, 'KwentasApp/currentproject.html')


def is_superuser(user):
    return user.is_authenticated and user.is_superuser

@user_passes_test(lambda u: u.is_superuser, login_url='login')
def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Your account has been created successfully!')
                return redirect('homepage')  # Use the name of your homepage URL pattern
            except Exception as e:
                messages.error(request, f'An error occurred: {e}')
        else:
            messages.error(request, 'Form is invalid. Please correct the errors.')
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
    print("homepage view called")  # Debugging print
    user_name = request.user.name if request.user.is_authenticated else "Guest"
    context = {
        'user_name': user_name,
        }
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
