from .celery import app as celery_app

# Expose the Celery app as a module-level variable for `celery -A event_platform` to find
__all__ = ('celery_app',)
