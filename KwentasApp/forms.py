# KwentasApp/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser  # Assuming you have a CustomUser model
from django.core.exceptions import ValidationError


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['username', 'name', 'email', 'department', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
       

    
        return cleaned_data

