# KwentasApp/apps.py

from django.apps import AppConfig

class KwentasAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'KwentasApp'

    def ready(self):
        import KwentasApp.signals  # Ensure signals are imported and connected
