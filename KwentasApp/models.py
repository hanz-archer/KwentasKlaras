# KwentasApp/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    department = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        # Set a default name based on the chosen department
        if not self.name and self.department:
            # Customize this logic based on your requirements
            default_name = f'Default Name for {self.department}'
            self.name = default_name

        super().save(*args, **kwargs)


from django.db import models

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

