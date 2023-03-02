from pathlib import Path

# Base path for Django
BASE_DIR = Path(__file__).parent.parent

# Secret key used for cookies
SECRET_KEY = 'django-insecure-8b0^zb*9fk0qmziby8wd(yz*^*sep$0%4$!9s(hz1#$%3@h1o@'

# Uncomment this line and add a custom message corresponding to your backup schedule
# AUTOBACKUP_MSG = 'Automatic backups are configured to run once an hour, but you may perform a manual backup.'

# Change to True if you would like to display a homepage (at main/templates/homepage.html)
HOMEPAGE = False

# Change to False in production
DEBUG = True

# Edit this to use your domain name
ALLOWED_HOSTS = ['spiritsoft.localhost']


# Active Django apps and components
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'main',
    'actions',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]
ROOT_URLCONF = 'SpiritSoft.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'main/templates'],
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
WSGI_APPLICATION = 'SpiritSoft.wsgi.application'

# Database - do not change
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
}

# Django default password checker - do not change
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Change these settings for your region
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'EST'
USE_I18N = True
USE_TZ = False

# Do not change
STATIC_URL = 'static/'

# Location to export static files
STATIC_ROOT = '/data/assets'
if DEBUG:
    STATIC_ROOT = 'compiledassets'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
