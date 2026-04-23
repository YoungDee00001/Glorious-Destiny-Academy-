"""
Django settings for GloriousProject project.
"""

import os
import dj_database_url
from pathlib import Path

# ------------------------------------------------------------
# BASE DIRECTORY
# ------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------------------------------------------------
# SECURITY SETTINGS
# ------------------------------------------------------------
SECRET_KEY = 'django-insecure-c&gs2e13$i5+8+oos%&wa!0=^+j0f)22#36=7@r14f)gbwk+y6'
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = ['*']

# ------------------------------------------------------------
# APPLICATIONS
# ------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    'django_crontab',

    "crispy_forms",
    "crispy_bootstrap5",
    'widget_tweaks',
    # 'channels',

    'accounts',
    'myPage',
    'dashboard',
    'administration',
    'birthdays',
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

# ------------------------------------------------------------
# DJANGO-CRON
# ------------------------------------------------------------
CRON_CLASSES = [
    "fees.cron.FeeReminderCronJob",
]
DJANGO_CRON_LOCK_BACKEND = 'django_cron.backends.lock.file.FileLock'
DJANGO_CRON_LOCK_TIME = 86400

CRONJOBS = [
    ('0 7 * * *', 'birthday.utils.check_and_send_birthday_emails'),
]

# ------------------------------------------------------------
# AUTH USER & CRISPY FORMS
# ------------------------------------------------------------
AUTH_USER_MODEL = 'accounts.User'
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# # ------------------------------------------------------------
# # CHANNELS (WebSocket)
# # ------------------------------------------------------------
# ASGI_APPLICATION = "GloriousProject.asgi.application"

# REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')

# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels_redis.core.RedisChannelLayer",
#         "CONFIG": {
#             "hosts": [REDIS_URL],
#         },
#     },
# }

# ------------------------------------------------------------
# MIDDLEWARE
# ------------------------------------------------------------
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
# DATABASE — PostgreSQL via Railway
# ------------------------------------------------------------
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL', f'sqlite:///{BASE_DIR / "db.sqlite3"}'),
        conn_max_age=600,
    )
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
TIME_ZONE = 'Africa/Lagos'
USE_I18N = True
USE_TZ = True

# ------------------------------------------------------------
# STATIC & MEDIA FILES
# ------------------------------------------------------------
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static_my_project"),
]

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# ------------------------------------------------------------
# DEFAULT PRIMARY KEY FIELD
# ------------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ------------------------------------------------------------
# EMAIL CONFIGURATION (Gmail SMTP)
# ------------------------------------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'gloriousdestinyacademygda@gmail.com'
EMAIL_HOST_PASSWORD = 'ilciltoavwlxrugl'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# ------------------------------------------------------------
# PAYSTACK CONFIGURATION
# ------------------------------------------------------------
PAYSTACK_PUBLIC_KEY = "pk_test_fe15622a8f8d6ee21a455627d7fe59b08bdf80f7"
PAYSTACK_SECRET_KEY = "sk_test_ce2a0d954fd5ae8945eaf4ac00f914a91a02f7f4"
PAYSTACK_INITIALIZE_URL = "https://api.paystack.co/transaction/initialize"
PAYSTACK_VERIFY_URL = "https://api.paystack.co/transaction/verify/"

# ------------------------------------------------------------
# LOGGING
# ------------------------------------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'fees': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# ------------------------------------------------------------
# AUTH OPTIONS
# ------------------------------------------------------------
LOGOUT_REDIRECT_URL = '/'