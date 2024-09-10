from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMultiAlternatives, BadHeaderError
from django.template.loader import render_to_string
from .forms import RegistrationForm
from .models import CustomUser  # Assuming you have a CustomUser model
import logging
import json
import random
import string
from django.http import HttpResponse
import openpyxl
import os
from io import BytesIO
from django.conf import settings
from openpyxl.styles import Font
from .projects import get_project_entries 

logger = logging.getLogger(__name__)

def download_xlsx(request, entry_code):
    # Fetch the specific project entry based on the entry code
    _, _, all_entries = get_project_entries()  # Fetch all project entries
    selected_entry = None
    
    for entry in all_entries:
        if entry['code'] == entry_code:
            selected_entry = entry
            break

    if not selected_entry:
        return HttpResponse("Entry not found", status=404)

    # Define the path to your pre-designed template
    template_path = os.path.join(settings.BASE_DIR, 'KwentasApp/static/KwentasApp/xls_templates/template_report.xlsx')

    # Load the pre-designed XLSX template
    wb = openpyxl.load_workbook(template_path)
    ws = wb.active

    calibri_bold_7 = Font(name='Calibri', bold=True, size=7)

    # Modify the necessary cells with dynamic data
    service_type = selected_entry.get('services', 'General')

    # Define different cell positions based on the service type
    if service_type == 'General':
        ppa_cell, location_cell, start_date_cell, end_date_cell, remarks_cell, total_disbursements_cell, overall_budget_cell = 'A12', 'B12', 'D12', 'E12', 'I12', 'G12', 'C12'
    elif service_type == 'Social':
        ppa_cell, location_cell, start_date_cell, end_date_cell, remarks_cell, total_disbursements_cell, overall_budget_cell = 'A12', 'B12', 'D12', 'E12', 'I12', 'G12', 'C12'
    elif service_type == 'Economic':
        ppa_cell, location_cell, start_date_cell, end_date_cell, remarks_cell, total_disbursements_cell, overall_budget_cell = 'A19', 'B19', 'D19', 'E19', 'I19', 'G19', 'C19'
    elif service_type == 'Environmental':
        ppa_cell, location_cell, start_date_cell, end_date_cell, remarks_cell, total_disbursements_cell, overall_budget_cell = 'A19', 'B19', 'D19', 'E19', 'I19', 'G19', 'C19'

    # Populate the cells with the dynamic data
    ws[ppa_cell] = selected_entry.get('ppa', '')
    ws[ppa_cell].font = calibri_bold_7
    
    ws[location_cell] = selected_entry.get('location', '')
    ws[location_cell].font = calibri_bold_7
    
    ws[start_date_cell] = selected_entry.get('start_date', '')
    ws[start_date_cell].font = calibri_bold_7
    
    ws[end_date_cell] = selected_entry.get('end_date', '')
    ws[end_date_cell].font = calibri_bold_7
    
    ws[remarks_cell] = selected_entry.get('remarks', '')
    ws[remarks_cell].font = calibri_bold_7
    
    ws[total_disbursements_cell] = selected_entry.get('total_disbursements', '')
    ws[total_disbursements_cell].font = calibri_bold_7
    
    ws[overall_budget_cell] = selected_entry.get('overall_budget', '')
    ws[overall_budget_cell].font = calibri_bold_7

    # Add obligations data if available
    obligations = selected_entry.get('obligations', [])
    row_num = 10
    for obligation in obligations:
        ws[f'A{row_num}'] = obligation.get('name', '')
        ws[f'B{row_num}'] = obligation.get('spent', '')
        ws[f'C{row_num}'] = obligation.get('date', '')
        row_num += 1

    # Set up the response as an Excel file download
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=Project-Code-{entry_code}-Report.xlsx'

    wb.save(response)
    return response


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







def logout_view(request):
    logout(request)
    return redirect(reverse('login'))




@login_required
def homepage(request):
    print("homepage view called")  # Debugging print
    user_name = request.user.name if request.user.is_authenticated else "Guest"
    context = {
        'user_name': user_name,
        }
    return render(request, 'KwentasApp/homepage.html', context)



def forgotpassword(request):
     if request.method == 'POST':
        email = request.POST.get('email')
        code = request.POST.get('code')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
     return render(request, 'KwentasApp/forgot-password.html')





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
    




               



