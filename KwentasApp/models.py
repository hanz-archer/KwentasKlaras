# KwentasApp/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
import pyotp

class CustomUser(AbstractUser):
    department = models.CharField(max_length=255)
    name = models.CharField(max_length=255, blank=True)
    totp_secret = models.CharField(max_length=32, default=pyotp.random_base32, blank=True, null=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        # Set a default name based on the chosen department
        if not self.name and self.department:
            self.name = f'Default Name for {self.department}'
        
        # Ensure that totp_secret is generated if not already set
        if not self.totp_secret:
            self.totp_secret = pyotp.random_base32()

        super().save(*args, **kwargs)


from django.conf import settings
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    two_factor_enabled = models.BooleanField(default=False)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    totp_secret = models.CharField(max_length=32, blank=True, null=True)

    def __str__(self):
        return self.user.username

class Entry(models.Model):
    code = models.CharField(max_length=100)
    ppa = models.CharField(max_length=255)
    implementing_unit = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    appropriation = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    remarks = models.TextField()
    remaining_balance = models.DecimalField(max_digits=10, decimal_places=2)
    total_spent = models.DecimalField(max_digits=10, decimal_places=2)
    added_budget = models.DecimalField(max_digits=10, decimal_places=2)
    total_budget = models.DecimalField(max_digits=10, decimal_places=2)
    utilization_rate = models.DecimalField(max_digits=5, decimal_places=2)
    # Add other fields and relationships as needed

    def __str__(self):
        return self.code
    

from django.db import models

class FirebaseEntry(models.Model):
    code = models.CharField(max_length=255)
    ppa = models.CharField(max_length=255)
    # Add other relevant fields here if needed

