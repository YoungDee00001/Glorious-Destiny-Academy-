"""
Django settings for GloriousProject project.
Merged / configured with email (Gmail) and Paystack settings.
"""

import os
from pathlib import Path

# ------------------------------------------------------------
# BASE DIRECTORY
# ------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------------------------------------------------
# SECURITY SETTINGS
# ------------------------------------------------------------
SECRET_KEY = 'django-insecure-c&gs2e13$i5+8+oos%&wa!0=^+j0f)22#36=7@r14f)gbwk+y6'
DEBUG = True
# ALLOWED_HOSTS = ['192.168.198.231','127.0.0.1']  # Update for production
ALLOWED_HOSTS = ['*']


# ------------------------------------------------------------
# APPLICATIONS
# ------------------------------------------------------------
INSTALLED_APPS = [
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # Cron apps (you can use either django_cron or django_crontab)
    # 'django_cron',        # optional: if you want django-cron style cron classes
    'django_crontab',
    

    # Third-party apps
    "crispy_forms",
    "crispy_bootstrap5",
    'widget_tweaks',
    'channels',

    # Local apps
    'accounts',
    'myPage',
    'dashboard',
    'administration',
    'birthdays',   # if you plan to use it
    'fees',
    'online_payments',
    'staff',
    'students',
    'superuser',
    'parent',
    'schoolevents',
    'notification',
    'chat',
    'reportcard',
    
]


# DJANGO-CRON CONFIGURATION
# ==================================================
CRON_CLASSES = [
    "fees.cron.FeeReminderCronJob",  # Automatic fee reminder cron job
]

# Cron settings (optional)
DJANGO_CRON_LOCK_BACKEND = 'django_cron.backends.lock.file.FileLock'
DJANGO_CRON_LOCK_TIME = 86400  # Lock time in seconds (24 hours)

# ==================================================
# TIMEZONE SETTINGS
# ==================================================
TIME_ZONE = 'Africa/Lagos'  # Set to your school's timezone
USE_TZ = True

# If you use django-crontab, configure CRONJOBS (example)
CRONJOBS = [
    # run birthdays check at 07:00 every day (example)
    ('0 7 * * *', 'birthday.utils.check_and_send_birthday_emails'),
    # you can also schedule your fees cron script here like:
    # ('0 8 * * *', 'fees.cron.send_fee_reminders'),  # if you create a CLI callable
]

# ------------------------------------------------------------
# AUTH USER & CRISPY FORMS
# ------------------------------------------------------------
AUTH_USER_MODEL = 'accounts.User'
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# ------------------------------------------------------------
# CHANNELS (WebSocket)
# ------------------------------------------------------------
ASGI_APPLICATION = "GloriousProject.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",  # Use Redis in production
    },
}

# ------------------------------------------------------------
# MIDDLEWARE
# ------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ------------------------------------------------------------
# URLS & TEMPLATES
# ------------------------------------------------------------
ROOT_URLCONF = 'GloriousProject.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'GloriousProject.wsgi.application'

# ------------------------------------------------------------
# DATABASE
# ------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ------------------------------------------------------------
# PASSWORD VALIDATION
# ------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ------------------------------------------------------------
# INTERNATIONALIZATION
# ------------------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Lagos'  # set to your preferred timezone
USE_I18N = True
USE_TZ = True

# ------------------------------------------------------------
# STATIC & MEDIA FILES
# ------------------------------------------------------------
STATIC_URL = 'static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static_my_project"),
]

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_cdn", "static_root")

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_cdn", "media_root")

# ------------------------------------------------------------
# DEFAULT PRIMARY KEY FIELD
# ------------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ------------------------------------------------------------
# EMAIL CONFIGURATION (Gmail SMTP)
# ------------------------------------------------------------
# You've already created an app password and provided it below.
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Use your school's email account
EMAIL_HOST_USER = 'gloriousdestinyacademygda@gmail.com'
EMAIL_HOST_PASSWORD = 'ilciltoavwlxrugl'  # <-- Gmail App Password (keep secret)
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Optional: in development you can use console backend:
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# ------------------------------------------------------------
# PAYSTACK CONFIGURATION
# ------------------------------------------------------------
PAYSTACK_PUBLIC_KEY = "pk_test_fe15622a8f8d6ee21a455627d7fe59b08bdf80f7"
PAYSTACK_SECRET_KEY = "sk_test_ce2a0d954fd5ae8945eaf4ac00f914a91a02f7f4"
PAYSTACK_INITIALIZE_URL = "https://api.paystack.co/transaction/initialize"
PAYSTACK_VERIFY_URL = "https://api.paystack.co/transaction/verify/"

# ------------------------------------------------------------
# LOGGING (optional but recommended)
# ------------------------------------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'fees_system.log',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'fees': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# ------------------------------------------------------------
# AUTH OPTIONS
# ------------------------------------------------------------
LOGOUT_REDIRECT_URL = '/'

# ------------------------------------------------------------
# SECURITY / PRODUCTION REMINDERS
# ------------------------------------------------------------
# When deploying to production:
# - Move SECRET_KEY, EMAIL_HOST_PASSWORD, PAYSTACK keys to environment variables.
# - Set DEBUG = False
# - Configure ALLOWED_HOSTS
# - Configure secure cookies, HSTS, SSL redirect, and X_FRAME_OPTIONS
# - Use a real channel layer backend (Redis) for Channels
#
# Example usage of env variables:
# EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
# PAYSTACK_SECRET_KEY = os.getenv('PAYSTACK_SECRET_KEY')
# SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')




import os

TERMII_API_KEY = os.getenv("TLiTiVpBmhUIcVNPYfsgszERYrXJDpCnBOSlXpQkTAIZPnJSzOobHimUymVhrZ")
TERMII_SENDER_ID = os.getenv("TERMII_SENDER_ID")
TERMII_MESSAGE_TYPE = '2'  # '2' for transactional, '1' for promotional
TERMII_DLT_TE_ID = os.getenv("TERMII_DLT_TE_ID")
TERMII_DLT_TEMPLATE_ID = os.getenv("TERMII_DLT_TEMPLATE_ID")