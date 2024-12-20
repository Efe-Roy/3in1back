
from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-s2v*ko$0$n&k^dy#t3h0i9i2t^$70l9l28*ez7-tgllzwk-hb0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['147.182.215.149', '127.0.0.1', 'fuscaliaycontraloria.com']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'storages',

    #Third Party App
    'Auth',
    'pqrsAPI',
    'contratacionAPI',
    'InspecciónAPI',
    'lawAPI',
    'ticketAPI',
    'sisbenAPI',
    

    # API SetUp
    'rest_framework',
    'rest_framework.authtoken',
    # 'rest_auth',
    "corsheaders",
    
    'import_export',

]

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/ 'templates'],
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

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

if DEBUG:
    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.sqlite3',
    #         'NAME': BASE_DIR / 'db.sqlite3',
    #     }
    # }

    # LOCAL DATABASE
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'procesosadministrativos', 
            'USER': 'postgres',
            'PASSWORD': 'admin',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
else:
    # ONLINE LIVE
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'roydb',
            'USER': 'royuser1',
            'PASSWORD': 'roy12345',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }

AUTH_USER_MODEL = 'Auth.User'

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

if DEBUG:
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

    # MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    # MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'three-in-one-static')
    MEDIA_URL = '/three-in-one-static/'
else:
    AWS_ACCESS_KEY_ID = 'DO00PRT6ALVZRZ9YPQ8K'
    AWS_SECRET_ACCESS_KEY = 'hlzEl2qyXWgINQuvEncA0HRri0gNZLblj+WqVZ8KNqw'
    AWS_STORAGE_BUCKET_NAME = 'three-in-one-space-bucket'
    AWS_S3_ENDPOINT_URL = 'https://sfo3.digitaloceanspaces.com'
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }
    AWS_LOCATION = 'three-in-one-static'

    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static'),
    ]
    STATIC_URL = 'https://%s/%s/' % (AWS_S3_ENDPOINT_URL, AWS_LOCATION)
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ]
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://167.71.19.13",
    "https://procesosadministrativos.com",
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    # 'Auth.authentication.EmailAuthBackend',
]

# DATA_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024 * 20
# FILE_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024 * 20
# MAX_UPLOAD_SIZE = 1024 * 1024 * 100 

# FILE_UPLOAD_HANDLERS = [
#     'django.core.files.uploadhandler.MemoryFileUploadHandler',
#     'django.core.files.uploadhandler.TemporaryFileUploadHandler',
# ]

if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
else:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_USE_SSL = True
    EMAIL_HOST = "smtp.hostinger.com"
    # EMAIL_HOST_USER = "info@licenciasurbanisticas.com"
    EMAIL_HOST_USER = "info@procesosadministrativos.com"
    # EMAIL_HOST_PASSWORD = "Email10.CD"
    EMAIL_HOST_PASSWORD = "Info10.CD"
    EMAIL_PORT = 465
