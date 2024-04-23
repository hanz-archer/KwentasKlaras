# KwentasApp/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    department = models.CharField(max_length=255)
    name = models.CharField(max_length=255)  # Remove the default value

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        # Set a default name based on the chosen department
        if not self.name and self.department:
            # Customize this logic based on your requirements
            default_name = f'Default Name for {self.department}'
            self.name = default_name

        super().save(*args, **kwargs)
