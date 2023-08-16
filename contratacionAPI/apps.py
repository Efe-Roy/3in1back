from django.apps import AppConfig


class ContratacionapiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'contratacionAPI'

    def ready(self):
        import contratacionAPI.signals