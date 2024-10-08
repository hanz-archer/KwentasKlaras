from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ValidationError
from .models import CustomUser
import random

class RegistrationForm(UserCreationForm):
    email = forms.EmailField()
    verification_code = forms.CharField(max_length=6, required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'name', 'email', 'department', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        self.generated_code = random.randint(100000, 999999)  # Generate a random 6-digit code
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        verification_code = cleaned_data.get('verification_code')
        if self.instance.pk is None:  # Only send email for new user creation
            # Assuming the email verification code is sent after form validation.
            self.send_verification_email(email)
        return cleaned_data

    def send_verification_email(self, email):
        send_mail(
            'Your Verification Code',
            f'Your verification code is {self.generated_code}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
