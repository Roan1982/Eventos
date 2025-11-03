from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# Basic env-driven configuration so the project can run in prod with Docker/Traefik
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-insecure-secret-key-change-in-prod')
DEBUG = os.environ.get('DEBUG', '1') not in ('0', 'False', 'false')

# ALLOWED_HOSTS can be a comma-separated list in the environment
raw_allowed = os.environ.get('ALLOWED_HOSTS', '')
if raw_allowed:
    ALLOWED_HOSTS = [h.strip() for h in raw_allowed.split(',') if h.strip()]
else:
    # default to localhost and 127.0.0.1 for local dev
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'accounts',
    'events',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'event_platform.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                    # add unread notifications count for navbar badge
                    'events.context_processors.unread_notifications_count',
            ],
        },
    },
]

WSGI_APPLICATION = 'event_platform.wsgi.application'

# Database: prefer Postgres via environment variables, fallback to sqlite
if os.environ.get('POSTGRES_DB'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('POSTGRES_DB'),
            'USER': os.environ.get('POSTGRES_USER'),
            'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
            'HOST': os.environ.get('DB_HOST', 'db'),
            'PORT': os.environ.get('DB_PORT', '5432'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
# Use whitenoise storage for compressed static files; works on Docker without extra server
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email: console backend for dev (can be overridden with env vars)
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')

# Public site URL used to build absolute links in emails. In production set SITE_URL to e.g. 'https://mishosts.ddns.net'
SITE_URL = os.environ.get('SITE_URL', '')
# Backwards-compatible alias used in places that expect DOMAIN
DOMAIN = os.environ.get('DOMAIN', SITE_URL)

# SMTP configuration (when deploying, set EMAIL_HOST to enable)
EMAIL_HOST = os.environ.get('EMAIL_HOST')
if EMAIL_HOST:
    EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
    EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', '1') not in ('0', 'False', 'false')
    EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
    DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER)
    SERVER_EMAIL = os.environ.get('SERVER_EMAIL', DEFAULT_FROM_EMAIL)

# Celery broker (used by background workers). Default points to the Redis
# service name used in docker-compose.prod.yml
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://redis:6379/0')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', CELERY_BROKER_URL)

# DRF basic config
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

# Upload limits (10MB)
MAX_UPLOAD_SIZE = 10 * 1024 * 1024
ALLOWED_CONTENT_TYPES = [
    'image/jpeg', 'image/png', 'image/gif',
    'video/mp4', 'video/webm',
]

# Auth configuration
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'  # Redirigir al home después del login
LOGOUT_REDIRECT_URL = '/'

# Security settings when DEBUG is False (production)
if not DEBUG:
    # Respect X-Forwarded-Proto header set by reverse proxy (Traefik)
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', '1') not in ('0', 'False', 'false')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = int(os.environ.get('SECURE_HSTS_SECONDS', '3600'))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = os.environ.get('SECURE_HSTS_INCLUDE_SUBDOMAINS', '1') not in ('0', 'False', 'false')
    SECURE_HSTS_PRELOAD = os.environ.get('SECURE_HSTS_PRELOAD', '0') not in ('0', 'False', 'false')
    # If you're behind a proxy that terminates TLS, set this to true
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
