# KwentasApp/admin.py

from django.contrib import admin
from .models import CustomUser
from unfold.admin import ModelAdmin

class CustomUserAdmin(ModelAdmin):
    list_display = ('username', 'email', 'department', 'is_staff')
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'department', 'name')}),  # Include 'name' here
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'department', 'name', 'password1', 'password2'),  # Include 'name' here
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
