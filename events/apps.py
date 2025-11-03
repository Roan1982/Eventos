from django.apps import AppConfig

class EventsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'events'
    def ready(self):
        # Import signals to ensure they're registered
        try:
            from . import signals  # noqa: F401
        except Exception:
            # Avoid import errors at startup causing the whole app to crash
            pass
