from django.apps import AppConfig
from authservice import signals


class AuthserviceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authservice'

    def ready(self):
       import authservice.signals  
        
