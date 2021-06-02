from pathlib import Path
import environ
import os

WSGI_APPLICATION = 'onemob.wsgi.application'

env = environ.Env()
# reading .env file
environ.Env.read_env(DEBUG=(bool, False))

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG')

ALLOWED_HOSTS = [env('ALLOWED_HOSTS'), 'localhost']


# Application definition

INSTALLED_APPS = [
    'virtualclass',
    # 'virtualclass.apps.VirtualclassConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_hosts',
    'rest_framework.authtoken',
    'corsheaders',
    'nested_admin',
    'payment',
]

MIDDLEWARE = [
    'django_hosts.middleware.HostsRequestMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_hosts.middleware.HostsResponseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]
AUTH_USER_MODEL = 'virtualclass.Student'


ROOT_URLCONF = 'androidserver.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'androidserver.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

if 'sqlite' in env('DATABASE'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
	}
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': env('DATABASE_NAME'),
            'USER': env('DATABASE_USER'),
            'PASSWORD': env('DATABASE_PASSWORD'),
            'HOST': '127.0.0.1',
            'PORT': '5432',
        }
    }

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = "/media/"
MEDIA_ROOT = str(BASE_DIR) + '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

DEFF_SALT = env('DEFF_SALT')
DEFF_PASSWORD = env('DEFF_PASS')
DEFF_FETCH_URL_NAME = 'api:video_fetch_url'

# django cors-headers
CORS_ORIGIN_ALLOW_ALL = True

# api rest_framework settings
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'virtualclass.authentication.ExpiringTokenAuthentication',
        # 'rest_framework.authentication.TokenAuthentication',
    ],
}
REST_FRAMEWORK_TOKEN_EXPIRE_HOURS = 1  # one hour
EMAIL_SENT_TIMEOUT = 60  # 60 seconds
ROOT_HOSTCONF = 'androidserver.hosts'
DEFAULT_HOST = 'index'
PARENT_HOST = 'localhost:8000'
IDPAY_API_KEY = env('IDPAY_API_KEY')
IDPAY_SANDBOX = env.bool('IDPAY_SANDBOX')
AUTH_HEADER_PREFIX = 'Token'

# if not DEBUG:
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS')
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_PORT = env.int('EMAIL_PORT')
# else:
#    EMAIL_BACKEND = (
#        'django.core.mail.backends.console.EmailBackend'
#    )
