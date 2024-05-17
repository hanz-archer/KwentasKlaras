from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .firebase import database
from django.http import JsonResponse
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.db.models import F, ExpressionWrapper, FloatField
from django.http import HttpResponse
from django.shortcuts import render
import firebase_admin
from firebase_admin import credentials, db
import datetime
import re
import re
import datetime
from django.http import HttpResponse
from django.shortcuts import render

def create_entry(request):
    if request.method == 'POST':
        # Extract data from the form submission
        ppa = request.POST.get('ppa')
        implementing_unit = request.POST.get('implementing_unit')
        location = request.POST.get('location')
        appropriation_str = request.POST.get('appropriation', '0')  # Default to '0' if not provided
        remarks = request.POST.get('remarks')
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        code = request.POST.get('code')
        services = request.POST.get('services')
        year_str = request.POST.get('year')
        
        # Validate required fields
        if not (ppa and implementing_unit and location and appropriation_str and start_date_str and end_date_str and code and services and year_str):
            return HttpResponse('<script>alert("All fields are required."); window.location.href = "/adddata";</script>', status=400)

        # Validate appropriation amount
        try:
            appropriation = float(appropriation_str)
            if appropriation <= 0:
                return HttpResponse('<script>alert("Appropriation amount must be a positive number."); window.location.href = "/adddata";</script>', status=400)
        except ValueError:
            return HttpResponse('<script>alert("Invalid appropriation amount."); window.location.href = "/adddata";</script>', status=400)

        # Validate date format
        date_format = r'\d{4}-\d{2}-\d{2}'  # YYYY-MM-DD
        if not (re.match(date_format, start_date_str) and re.match(date_format, end_date_str)):
            return HttpResponse('<script>alert("Invalid date format. Please use YYYY-MM-DD."); window.location.href = "/adddata";</script>', status=400)

        # Convert dates to datetime objects for further validation
        try:
            start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d')
        except ValueError:
            return HttpResponse('<script>alert("Invalid date."); window.location.href = "/adddata";</script>', status=400)

        # Validate start date is before end date
        if start_date >= end_date:
            return HttpResponse('<script>alert("Start date must be before end date."); window.location.href = "/adddata";</script>', status=400)

        # Validate code format
        if not re.match(r'^[\w\d\s-]+$', code):
            return HttpResponse('<script>alert("Invalid code format. Only letters, numbers, spaces, and hyphens are allowed."); window.location.href = "/adddata";</script>', status=400)

        # Validate code uniqueness
        if database.child('Data').child(code).get().val() is not None:
            return HttpResponse('<script>alert("Code already exists."); window.location.href = "/adddata";</script>', status=400)

        # Validate year format
        if not re.match(r'\d{4}', year_str):
            return HttpResponse('<script>alert("Invalid year format. Please use YYYY."); window.location.href = "/adddata";</script>', status=400)

        # Set remaining balance equal to appropriation
        total_budget = appropriation
        remaining_balance = total_budget

        try:
            # Save project entry with code as the key
            new_entry_ref = database.child('Data').child(code).set({
                "ppa": ppa,
                "implementing_unit": implementing_unit,
                "location": location,
                "appropriation": appropriation,
                "remarks": remarks,
                "start_date": start_date_str,
                "end_date": end_date_str,
                "code": code,
                "services": services,
                "year": year_str,
                "remaining_balance": remaining_balance,
                "total_spent": 0,  # Set total spent default value to 0
                "added_budget": 0,  # Set added budget default value to 0
                "total_budget": total_budget
            })
            
            return HttpResponse('<script>alert("Successfully added"); window.location.href = "/adddata";</script>')
          
        except Exception as e:
            return HttpResponse(f'<script>alert("Error: {str(e)}"); window.location.href = "/adddata";</script>', status=500)
    else:
        # Render the form for GET requests
        return render(request, 'KwentasApp/adddata.html')



def adddata(request):
    return render(request, 'KwentasApp/adddata.html')




def continuing_add_obligation(request):
    if request.method == 'POST':
        entry_key = request.POST.get('entry-code')
        name = request.POST.get('obligation_name')
        spent = float(request.POST.get('obligation_spent', 0))
        date = request.POST.get('obligation_date')

        try:
            entry_ref = database.child('Data').child(entry_key)  # Assigning database child to entry_ref

            # Get data for the entry
            entry_data = entry_ref.get().val()

            # Check if entry_data is None
            if entry_data is None:
                return HttpResponse('<script>alert("Entry not found."); window.location.href = "/";</script>', status=404)

            # Update total spent for the entry
            total_spent = entry_data.get('total_spent', 0) + spent

            # Calculate remaining balance
            total_budget = entry_data.get('total_budget', 0)
            remaining_balance = total_budget - total_spent

            if remaining_balance < 0:
                  return HttpResponse('<script>alert("Remaining Balance cant be negative. Add Budget if you wish to continue"); window.location.href = "/continuing_projects";</script>', status=404)
            # Push a new child node with a unique key for the obligation under the chosen entry
            new_obligation_ref = database.child('Data').child(entry_key) .child('obligation').push({
                'name': name,
                'spent': spent,
                'date': date
            })

            # Update total spent under the entry
            database.child('Data').child(entry_key) .update({"total_spent": total_spent})

            # Update remaining balance under the entry
            database.child('Data').child(entry_key) .update({"remaining_balance": remaining_balance})

            # Redirect back to the previous page
            return redirect(request.META.get('HTTP_REFERER', '/'))
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}", status=500)
    else:
        return HttpResponse("Method not allowed", status=405)







def ongoing_add_obligation(request):
    if request.method == 'POST':
        entry_key = request.POST.get('entry-code')
        name = request.POST.get('obligation_name')
        spent = float(request.POST.get('obligation_spent', 0))
        date = request.POST.get('obligation_date')

        try:
            entry_ref = database.child('Data').child(entry_key)  # Assigning database child to entry_ref

            # Get data for the entry
            entry_data = entry_ref.get().val()

            # Check if entry_data is None
            if entry_data is None:
                return HttpResponse('<script>alert("Entry not found."); window.location.href = "/";</script>', status=404)

            # Update total spent for the entry
            total_spent = entry_data.get('total_spent', 0) + spent

            # Calculate remaining balance
            total_budget = entry_data.get('total_budget', 0)
            remaining_balance = total_budget - total_spent

            if remaining_balance < 0:
                  return HttpResponse('<script>alert("Remaining Balance cant be negative. Add Budget if you wish to continue"); window.location.href = "/ongoing_projects";</script>', status=404)
            # Push a new child node with a unique key for the obligation under the chosen entry
            new_obligation_ref = database.child('Data').child(entry_key) .child('obligation').push({
                'name': name,
                'spent': spent,
                'date': date
            })

            # Update total spent under the entry
            database.child('Data').child(entry_key) .update({"total_spent": total_spent})

            # Update remaining balance under the entry
            database.child('Data').child(entry_key) .update({"remaining_balance": remaining_balance})

            # Redirect back to the previous page
            return redirect(request.META.get('HTTP_REFERER', '/'))
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}", status=500)
    else:
        return HttpResponse("Method not allowed", status=405)























from django.shortcuts import render, redirect, HttpResponse



def add_budget(request):
    if request.method == 'POST':
        entry_key = request.POST.get('entry_code')
        name = request.POST.get('budget_name')
        added_budget = float(request.POST.get('added_budget', 0))
        date = request.POST.get('budget_date')

        try:
            # Get data for the entry
            entry_data = database.child('Data').child(entry_key).get().val()

            # Check if entry_data is None
            if entry_data is None:
                return HttpResponse('<script>alert("Entry not found."); window.location.href = "/";</script>', status=404)

            # Calculate total added budget
            total_added_budget = entry_data.get('added_budget', 0) + added_budget

            # Calculate overall total budget
            total_budget = entry_data.get('total_budget', 0)
            overall_budget = total_budget + added_budget

            # Calculate remaining balance
            remaining_balance = entry_data.get('remaining_balance', 0) + added_budget

            # Check if remaining balance would go below 0
            if remaining_balance < 0:
                return HttpResponse('<script>alert("Remaining balance cannot go below 0."); window.location.href = "/";</script>', status=400)

            # Push a new child node with a unique key for the budget under the chosen entry
            new_budget_ref = database.child('Data').child(entry_key).child('budget').push({
                'name': name,
                'added_budget': added_budget,
                'date': date
            })

            # Update added_budget, total_budget, and remaining_balance under the entry
            database.child('Data').child(entry_key).update({
                "added_budget": total_added_budget,
                "total_budget": overall_budget,
                "remaining_balance": remaining_balance
            })

            return redirect(request.META.get('HTTP_REFERER', '/')) # Redirect back to the main projects page after successful addition
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}", status=500)
    else:
        return HttpResponse("Method not allowed", status=405)









from django.shortcuts import render

def get_project_entries():
    result = database.child('Data').get()

    entries_below_2024 = []
    entries_2024_and_above = []
    all_entries = []

    if result.val():
        for key, value in result.val().items():
            entry = {
                'ppa': value.get('ppa'),
                'implementing_unit': value.get('implementing_unit'),
                'location': value.get('location'),
                'appropriation': value.get('appropriation'),
                'remarks': value.get('remarks'),
                'start_date': value.get('start_date'),
                'end_date': value.get('end_date'),
                'code': value.get('code'),
                'services': value.get('services'),
                'year': value.get('year'),
                'remaining_balance': value.get('remaining_balance'),
                'total_spent': value.get('total_spent'),
                'added_budget': value.get('added_budget'),
                'total_budget': value.get('total_budget'),
                'obligation': []  # Initialize obligation list
            }
            # Check if obligation node exists
            if 'obligation' in value:
                # Iterate over obligation items and append to entry's obligation list
                for obligation_key, obligation_value in value['obligation'].items():
                    entry['obligation'].append({
                        'name': obligation_value.get('name'),
                        'spent': obligation_value.get('spent'),
                        'date': obligation_value.get('date')
                    })
            
            # Fetch budget data for the current entry
            budget_data = database.child('Data').child(key).child('budget').get().val()

            # Add budget data to the entry
            entry['budget_data'] = []
            if budget_data:
                for budget_key, budget_value in budget_data.items():
                    entry['budget_data'].append({
                        'name': budget_value.get('name'),
                        'added_budget': budget_value.get('added_budget'),
                        'date': budget_value.get('date')
                    })
            
            # Add entry to all_entries list
            all_entries.append(entry)

            # Check the year and add to the appropriate list
            if entry.get('year') is not None:
                if int(entry['year']) < 2024:
                    entries_below_2024.append(entry)
                else:
                    entries_2024_and_above.append(entry)
    
    return entries_below_2024, entries_2024_and_above, all_entries

def continuing_projects(request):
    entries_below_2024, _, all_entries = get_project_entries()
    return render(request, 'KwentasApp/continuing.html', {
        'entries_below_2024': entries_below_2024,
        'all_entries': all_entries
    })

def ongoing_projects(request):
    _, entries_2024_and_above, all_entries = get_project_entries()
    return render(request, 'KwentasApp/ongoing.html', {
        'entries_2024_and_above': entries_2024_and_above,
        'all_entries': all_entries
    })









def search_continuing_projects(request):
    query = request.GET.get('query')
    entries_below_2024 = []

    # Assuming you have a function to fetch ongoing projects from Firebase or database
    result = database.child('Data').get()

    if result.val():
        for key, value in result.val().items():
            entry = {
                'ppa': value.get('ppa'),
                'implementing_unit': value.get('implementing_unit'),
                'location': value.get('location'),
                'appropriation': value.get('appropriation'),
                'remarks': value.get('remarks'),
                'start_date': value.get('start_date'),
                'end_date': value.get('end_date'),
                'code': value.get('code'),
                'services': value.get('services'),
                'year': value.get('year'),
                'remaining_balance': value.get('remaining_balance'),
                'total_spent': value.get('total_spent'),
                'obligation': []  # Initialize obligation list
            }
            # Check if obligation node exists
            if 'obligation' in value:
                # Iterate over obligation items and append to entry's obligation list
                for obligation_key, obligation_value in value['obligation'].items():
                    entry['obligation'].append({
                        'name': obligation_value.get('name'),
                        'spent': obligation_value.get('spent'),
                        'date': obligation_value.get('date')
                    })

            # Check if the entry matches the search query
            if (query.lower() in str(entry['ppa']).lower() or
                query.lower() in str(entry['implementing_unit']).lower() or
                query.lower() in str(entry['location']).lower() or
                query.lower() in str(entry['appropriation']).lower() or
                query.lower() in str(entry['remarks']).lower() or
                query.lower() in str(entry['start_date']).lower() or
                query.lower() in str(entry['end_date']).lower() or
                query.lower() in str(entry['code']).lower() or
                query.lower() in str(entry['services']).lower()):
                
                if entry.get('year') is not None and int(entry['year']) < 2024:
                    entries_below_2024.append(entry)

    return render(request, 'KwentasApp/continuing.html', {'matched_entries_below_2024': entries_below_2024, 'query': query})



def search_ongoing_projects(request):
    query = request.GET.get('query')
    entries_2024_and_above = []

    # Assuming you have a function to fetch current projects from Firebase or database
    result = database.child('Data').get()

    if result.val():
        for key, value in result.val().items():
            entry = {
                'ppa': value.get('ppa'),
                'implementing_unit': value.get('implementing_unit'),
                'location': value.get('location'),
                'appropriation': value.get('appropriation'),
                'remarks': value.get('remarks'),
                'start_date': value.get('start_date'),
                'end_date': value.get('end_date'),
                'code': value.get('code'),
                'services': value.get('services'),
                'year': value.get('year'),
                'remaining_balance': value.get('remaining_balance'),
                'total_spent': value.get('total_spent'),
                'obligation': []  # Initialize obligation list
            }
            # Check if obligation node exists
            if 'obligation' in value:
                # Iterate over obligation items and append to entry's obligation list
                for obligation_key, obligation_value in value['obligation'].items():
                    entry['obligation'].append({
                        'name': obligation_value.get('name'),
                        'spent': obligation_value.get('spent'),
                        'date': obligation_value.get('date')
                    })

                # Check if the entry matches the search query
            if (query.lower() in str(entry['ppa']).lower() or
                    query.lower() in str(entry['implementing_unit']).lower() or
                    query.lower() in str(entry['location']).lower() or
                    query.lower() in str(entry['appropriation']).lower() or
                    query.lower() in str(entry['remarks']).lower() or
                    query.lower() in str(entry['start_date']).lower() or
                    query.lower() in str(entry['end_date']).lower() or
                    query.lower() in str(entry['code']).lower() or
                    query.lower() in str(entry['services']).lower()):
                
                if entry.get('year') is not None and int(entry['year']) >= 2024:
                    entries_2024_and_above.append(entry)

    return render(request, 'KwentasApp/ongoing.html', {'matched_entries_2024_and_above': entries_2024_and_above, 'query': query})





import re
import datetime
from django.shortcuts import render, redirect, HttpResponse

def ongoing_update_entry(request):
    if request.method == 'POST':
        entry_key = request.POST.get('entry_code')
        ppa = request.POST.get('ppa', '')  
        implementing_unit = request.POST.get('implementing_unit', '')  
        start_date_str = request.POST.get('start_date', '') 
        end_date_str = request.POST.get('end_date', '') 
        year_str = request.POST.get('year', '') 
        code = request.POST.get('code', '')  # Added code field
        services = request.POST.get('services', '')  # Added code field
        remarks = request.POST.get('remarks', '')  # Added code field
        location = request.POST.get('location', '')  # Added code field

        # Validate date format if not empty
        if start_date_str and end_date_str:
            date_format = r'\d{4}-\d{2}-\d{2}'  # YYYY-MM-DD
            if not (re.match(date_format, start_date_str) and re.match(date_format, end_date_str)):
                return HttpResponse('<script>alert("Invalid date format. Please use YYYY-MM-DD."); window.location.href = "/ongoing_projects";</script>', status=400)

            # Convert dates to datetime objects for further validation
            try:
                start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
                end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d')
            except ValueError:
                return HttpResponse('<script>alert("Invalid date."); window.location.href = "/ongoing_projects";</script>', status=400)

            # Validate start date is before end date
            if start_date >= end_date:
                return HttpResponse('<script>alert("Start date must be before end date."); window.location.href = "/ongoing_projects";</script>', status=400)

        # Validate year format if not empty
        if year_str:
            if not re.match(r'\d{4}', year_str):
                return HttpResponse('<script>alert("Invalid year format. Please use YYYY."); window.location.href = "/ongoing_projects";</script>', status=400)

        try:
            # Get data for the entry
            entry_data = database.child('Data').child(entry_key).get().val()

            # Check if entry_data is None
            if entry_data is None:
                return HttpResponse('<script>alert("Entry not found."); window.location.href = "/ongoing_projects";</script>', status=404)

            # Check if the code is being changed and if it already exists
            if code != entry_key and database.child('Data').child(code).get().val() is not None:
                return HttpResponse('<script>alert("Code already exists."); window.location.href = "/ongoing_projects";</script>', status=400)

            # Populate with previous values if fields are empty
            if not ppa:
                ppa = entry_data.get('ppa', '')
            if not implementing_unit:
                implementing_unit = entry_data.get('implementing_unit', '')
            if not start_date_str:
                start_date_str = entry_data.get('start_date', '')
            if not end_date_str:
                end_date_str = entry_data.get('end_date', '')
            if not year_str:
                year_str = entry_data.get('year', '')

            # Update other fields if provided
            database.child('Data').child(entry_key).update({
                "ppa": ppa,
                "implementing_unit": implementing_unit,
                "start_date": start_date_str,
                "end_date": end_date_str,
                "year": year_str,
                "code": code,  
                 "services": services,
                 "location": location,
                  "remarks": remarks
            })

            return redirect(request.META.get('HTTP_REFERER', '/')) # Redirect back to the main projects page after successful addition
        except Exception as e:
            return HttpResponse(f'<script>alert("Error: {str(e)}"); window.location.href = "/ongoing_projects";</script>', status=500)
    else:
        return HttpResponse('<script>alert("Method not allowed"); window.location.href = "/ongoing_projects";</script>', status=405)






def continuing_update_entry(request):
    if request.method == 'POST':
        entry_key = request.POST.get('entry_code')
        ppa = request.POST.get('ppa', '')  
        implementing_unit = request.POST.get('implementing_unit', '')  
        start_date_str = request.POST.get('start_date', '') 
        end_date_str = request.POST.get('end_date', '') 
        year_str = request.POST.get('year', '') 
        code = request.POST.get('code', '')  # Added code field
        services = request.POST.get('services', '')  # Added code field
        remarks = request.POST.get('remarks', '')  # Added code field
        location = request.POST.get('location', '')  # Added code field

        # Validate date format if not empty
        if start_date_str and end_date_str:
            date_format = r'\d{4}-\d{2}-\d{2}'  # YYYY-MM-DD
            if not (re.match(date_format, start_date_str) and re.match(date_format, end_date_str)):
                return HttpResponse('<script>alert("Invalid date format. Please use YYYY-MM-DD."); window.location.href = "/ongoing_projects";</script>', status=400)

            # Convert dates to datetime objects for further validation
            try:
                start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
                end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d')
            except ValueError:
                return HttpResponse('<script>alert("Invalid date."); window.location.href = "/continuing_projects";</script>', status=400)

            # Validate start date is before end date
            if start_date >= end_date:
                return HttpResponse('<script>alert("Start date must be before end date."); window.location.href = "/continuing_projects";</script>', status=400)

        # Validate year format if not empty
        if year_str:
            if not re.match(r'\d{4}', year_str):
                return HttpResponse('<script>alert("Invalid year format. Please use YYYY."); window.location.href = "/continuing_projects";</script>', status=400)

        try:
            # Get data for the entry
            entry_data = database.child('Data').child(entry_key).get().val()

            # Check if entry_data is None
            if entry_data is None:
                return HttpResponse('<script>alert("Entry not found."); window.location.href = "/continuing_projects";</script>', status=404)

            # Check if the code is being changed and if it already exists
            if code != entry_key and database.child('Data').child(code).get().val() is not None:
                return HttpResponse('<script>alert("Code already exists."); window.location.href = "/continuing_projects";</script>', status=400)

            # Populate with previous values if fields are empty
            if not ppa:
                ppa = entry_data.get('ppa', '')
            if not implementing_unit:
                implementing_unit = entry_data.get('implementing_unit', '')
            if not start_date_str:
                start_date_str = entry_data.get('start_date', '')
            if not end_date_str:
                end_date_str = entry_data.get('end_date', '')
            if not year_str:
                year_str = entry_data.get('year', '')

            # Update other fields if provided
            database.child('Data').child(entry_key).update({
                "ppa": ppa,
                "implementing_unit": implementing_unit,
                "start_date": start_date_str,
                "end_date": end_date_str,
                "year": year_str,
                "code": code,  
                 "services": services,
                 "location": location,
                  "remarks": remarks
            })

            return redirect(request.META.get('HTTP_REFERER', '/')) # Redirect back to the main projects page after successful addition
        except Exception as e:
            return HttpResponse(f'<script>alert("Error: {str(e)}"); window.location.href = "/continuing_projects";</script>', status=500)
    else:
        return HttpResponse('<script>alert("Method not allowed"); window.location.href = "/continuing_projects";</script>', status=405)





def continuing_delete_entry(request):
 
    if request.method == 'POST':
        entry_key = request.POST.get('entry_code')

        try:


          database.child('Data').child(entry_key).remove()
          return redirect(request.META.get('HTTP_REFERER', '/'))
        except Exception as e:
           return HttpResponse(f'<script>alert("Error: {str(e)}"); window.location.href = "/continuing_projects";</script>', status=500)
    else:
     return redirect('continuing_projects')  
    






def ongoing_delete_entry(request):
 
    if request.method == 'POST':
        entry_key = request.POST.get('entry_code')

        try:


          database.child('Data').child(entry_key).remove()
          return redirect(request.META.get('HTTP_REFERER', '/'))
        except Exception as e:
           return HttpResponse(f'<script>alert("Error: {str(e)}"); window.location.href = "/ongoing_projects";</script>', status=500)
    else:
     return redirect('ongoing_projects')  