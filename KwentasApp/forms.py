# KwentasApp/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser  # Assuming you have a CustomUser model

class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['username', 'name', 'email', 'department', 'password1', 'password2']
