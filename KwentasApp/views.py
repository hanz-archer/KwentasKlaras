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
        logger.info(f'Attempting login for user: {username}')  # Add logging

        user = authenticate(request, username=username, password=password)

        if user is not None:
            logger.info(f'Successful login for user: {username}')
            login(request, user)
            request.session['just_logged_in'] = True
            return redirect(reverse('homepage'))
        else:
            logger.warning(f'Invalid login attempt for user: {username}')
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


def forgotpassword(request):
     if request.method == 'POST':
        email = request.POST.get('email')
        code = request.POST.get('code')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
     return render(request, 'KwentasApp/forgot-password.html')


import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMultiAlternatives, BadHeaderError
from django.template.loader import render_to_string
from django.contrib.auth.hashers import make_password
from .models import CustomUser  # Assuming you have a CustomUser model
import random
import string
import json

logger = logging.getLogger(__name__)

@csrf_exempt
def send_verification_code(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            if email:
                code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
                subject = 'Your Verification Code'
                from_email = 'kwentasklarasboljoon@gmail.com'
                text_content = f'Your verification code is: {code}'

                try:
                    html_content = render_to_string('KwentasApp/verification_email.html', {'code': code})
                except Exception as e:
                    logger.error(f'Error rendering email template: {str(e)}')
                    return JsonResponse({'success': False, 'error': 'Error rendering email template.'}, status=500)

                try:
                    msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()
                    request.session['verification_code'] = code  # Store the code in the session
                    request.session['email'] = email  # Store the email in the session
                    logger.info(f'Verification code sent to {email}')
                    return JsonResponse({'success': True})
                except BadHeaderError:
                    logger.error(f'Invalid header found when sending email to {email}')
                    return JsonResponse({'success': False, 'error': 'Invalid header found.'}, status=400)
                except Exception as e:
                    logger.error(f'Error sending email to {email}: {str(e)}')
                    return JsonResponse({'success': False, 'error': 'Error sending email.'}, status=500)
            else:
                logger.warning('No email provided in the request.')
                return JsonResponse({'success': False, 'error': 'Invalid email'}, status=400)
        except json.JSONDecodeError:
            logger.warning('JSON decode error.')
            return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            logger.error(f'Unexpected error: {str(e)}')
            return JsonResponse({'success': False, 'error': 'Internal server error.'}, status=500)
    else:
        logger.warning('Invalid request method.')
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

import logging
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from .models import CustomUser  # Assuming you have a CustomUser model

logger = logging.getLogger(__name__)

@csrf_exempt
def verify_and_change_password(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            code = data.get('code')
            password = data.get('password')
            stored_code = request.session.get('verification_code')

            if code and code == stored_code and email == request.session.get('email'):
                user = CustomUser.objects.get(email=email)
                hashed_password = make_password(password)
                user.password = hashed_password
                user.save()

                # Log the user password hash
                logger.info(f'Password hash for user {email}: {hashed_password}')
                
                # Clear the session data
                del request.session['verification_code']
                del request.session['email']
                
                # Log successful password change
                logger.info(f'Password changed for user: {email}')

                # Attempt to log in the user with the new password
                user = authenticate(username=user.username, password=password)
                if user is not None:
                    login(request, user)
                    return JsonResponse({'success': True})
                else:
                    logger.error(f'Authentication failed for user after password change: {email}')
                    return JsonResponse({'success': False, 'error': 'Authentication failed after password change'}, status=400)
            else:
                logger.warning(f'Invalid code or email mismatch for user: {email}')
                return JsonResponse({'success': False, 'error': 'Invalid code or email mismatch'}, status=400)
        except json.JSONDecodeError:
            logger.warning('JSON decode error during password change process.')
            return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
        except CustomUser.DoesNotExist:
            logger.error(f'User not found for email: {email}')
            return JsonResponse({'success': False, 'error': 'User not found'}, status=404)
        except Exception as e:
            logger.error(f'Unexpected error during password change process: {str(e)}')
            return JsonResponse({'success': False, 'error': 'Internal server error.'}, status=500)
    else:
        logger.warning('Invalid request method for password change.')
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)
    




               



