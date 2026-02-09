from pathlib import Path
import sys
import environ

env = environ.Env()
environ.Env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

sys.path.append(str(BASE_DIR / "src"))

SECRET_KEY = env('SECRET_KEY')

DEBUG = env.bool('DEBUG', default=False)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'rest_framework',
    'drf_spectacular',
    
    'src.apps.rates',
    'src.apps.integrations', 
    'src.apps.common',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    'src.apps.common.middleware.SignatureCRC32Middleware',
]

ROOT_URLCONF = 'config.urls'

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'NBRB Currency Rates API',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


DATABASES = {
    'default': env.db('DATABASE_URL')
}


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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{asctime} [{levelname}] {name}:{lineno} - {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'src': {
            'handlers': ['console'],
            'level': 'INFO', 
            'propagate': True,
        },
        'django': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
        'httpx': {
            'handlers': ['console'],
            'level': 'WARNING', 
        },
    }
}
