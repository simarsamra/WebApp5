import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR.parent, '.env'))

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# Add 'staticfiles' app to INSTALLED_APPS if not already present
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',  # Ensure this is present
    'import_export',
    'maintenance',
]

# Directory where static files will be collected
STATIC_ROOT = str(BASE_DIR / 'staticfiles')

# Additional locations of static files
STATICFILES_DIRS = [
    str(BASE_DIR / 'maintenance' / 'static'),
]

# Print paths for debugging
print(f"BASE_DIR: {BASE_DIR}")
print(f"STATIC_ROOT: {STATIC_ROOT}")
print(f"STATICFILES_DIRS: {STATICFILES_DIRS}")
print("USING SETTINGS FILE:", __file__)

# Debug settings
SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret-key')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'maintenance', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Email backend for development: prints emails to the console
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# If you want to use a local SMTP server, comment the above and uncomment below:
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'localhost'
# EMAIL_PORT = 1025  # Change if your local SMTP uses a different port
# EMAIL_HOST_USER = ''
# EMAIL_HOST_PASSWORD = ''
# EMAIL_USE_TLS = False

# Default sender email address
DEFAULT_FROM_EMAIL = 'battery-tracker@example.com'

# Recipients for battery replacement reminders (comma-separated string or list)
REMINDER_RECIPIENTS = [
    'recipient1@example.com',
    'recipient2@example.com',
]

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'