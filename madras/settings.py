"""
Django settings for madras project.

Generated by 'django-admin startproject' using Django 1.8.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import dj_database_url
import raven

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# URL of the page to redirect to after a new user has confirmed their email
EMAIL_REDIRECT_URL = "https://apply.totalityhacks.com/#login"
EMAIL_REDIRECT_FAILURE_URL = "https://apply.totalityhacks.com/#resend"


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    "SECRET_KEY", "=u!#c-2hid%(4lq3w--$64!%qmbmmo-ae=l2_&*jpf47l84iv4")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", "true").lower() == "true"

AUTH_USER_MODEL = "registration.User"

# Allow all host headers
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'django_extensions',
    'rest_framework',
    'rest_framework.authtoken',
    'apps.checkin',
    'apps.reader',
    'apps.registration',
    'apps.application',
    'apps.stats',
    'apps.constants',
    'apps.locations',
    'apps.events',
    'apps.announcements',
    'fcm_django'
)

FCM_DJANGO_SETTINGS = {
        "FCM_SERVER_KEY": os.environ.get("FCM_SERVER_KEY"),
}

if not DEBUG:
    INSTALLED_APPS = INSTALLED_APPS + (
        'raven.contrib.django.raven_compat',
    )

MIDDLEWARE_CLASSES = (
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

CORS_ORIGIN_ALLOW_ALL = True  # who needs security anyway

ROOT_URLCONF = 'madras.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'madras.wsgi.application'

try:
    raven_release = raven.fetch_git_sha(os.path.abspath(os.pardir))
except Exception:
    raven_release = "unknown"

# Sentry logging settings
RAVEN_CONFIG = {
    'dsn': os.environ.get("SENTRY_DSN"),
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    'release': raven_release,
}


if 'SENDGRID_USERNAME' in os.environ:
    EMAIL_HOST = 'smtp.sendgrid.net'
    EMAIL_HOST_USER = os.environ.get("SENDGRID_USERNAME")
    EMAIL_HOST_PASSWORD = os.environ.get("SENDGRID_PASSWORD")
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True

    DEFAULT_FROM_EMAIL = 'noreply@totalityhacks.com'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    )
}

# disable documentation in production
if not DEBUG:
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
        'rest_framework.renderers.JSONRenderer',
    )

AUTHENTICATION_BACKENDS = ['apps.registration.backends.EmailBackend']

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': (
            'django.contrib.auth.password_validation'
            '.UserAttributeSimilarityValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.MinimumLengthValidator'),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.CommonPasswordValidator'),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation'
            '.NumericPasswordValidator'
        ),
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Heroku settings below
# Parse database configuration from $DATABASE_URL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
DATABASES['default'].update(dj_database_url.config())

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

AWS_REGION = os.environ.get("AWS_REGION")
AWS_S3_BUCKET_NAME = os.environ.get("AWS_S3_BUCKET_NAME")
AWS_SERVER_PUBLIC_KEY = os.environ.get("AWS_SERVER_PUBLIC_KEY")
AWS_SERVER_SECRET_KEY = os.environ.get("AWS_SERVER_SECRET_KEY")

# If not in debug mode, make sure to redirect to SSL.
if not DEBUG:
    SECURE_SSL_REDIRECT = True


GITHUB_USERNAME = os.environ.get("GITHUB_USERNAME")
GITHUB_PASSWORD = os.environ.get("GITHUB_PASSWORD")

# max size of resume (in bytes)
MAX_RESUME_SIZE = 4 * 1024 * 1024

# total number of reviews per application
TOTAL_NUM_REVIEWS = 5

# used for determining if user is staff or applicant
STAFF_EMAIL_SUFFIX = "totalityhacks.com"

# redirect to root on login (without next parameter)
LOGIN_REDIRECT_URL = "/"
