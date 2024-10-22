import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from django.core.management.utils import get_random_secret_key


BASE_DIR = Path(__file__).resolve().parent.parent


if not os.getenv('dockerenv'):
    print('local')
    load_dotenv()
    
    DEBUG = True
    RESULT_HOST = 'localhost:8000'
    SITE_ID = 2
    
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        }
    }   

    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": "redis://127.0.0.1:6380",
            # "LOCATION": "redis://redis:6379",
        }
    }

    # CELERY_BROKER_URL = 'amqp://localhost:5672/'
    CELERY_BROKER_URL = 'redis://localhost:6380/'
    REDIS_HOST = 'localhost'
    REDIS_PORT = '6380'



SECRET_KEY = os.environ.get('SECRET_KEY')

if not SECRET_KEY:
    # Генерация нового ключа, если его нет в переменных окружения
    SECRET_KEY = get_random_secret_key()
    print(f'Generated new SECRET_KEY: {SECRET_KEY}')



ALLOWED_HOSTS = ['localhost', '127.0.0.1',
                 'auto-subs.ru', 'subs', 
                 'auto-subs', 'autosubs', 
                 '192.168.0.109', 'webapp', ]

CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:1337',
                        'http://127.0.0.1:8000',
                        'http://127.0.0.1:8002',
                        'http://127.0.0.1', 
                        'http://localhost:1337', 
                        'https://yourdomain.com']

USE_X_FORWARDED_HOST = True
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SOCIAL_AUTH_REDIRECT_IS_HTTPS = True
# SOCIAL_AUTH_GITHUB_REDIRECT_URI = 'http://127.0.0.1:1337/social_auth/complete/github/'





INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_extensions',
    'corsheaders',
    'rest_framework',
    'social_django',
    
    'web_app_auto_subs.apps.WebAppAutoSubsConfig',
    
    'django.contrib.sites',
    
    'django_telegram_login',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'auto_subs.urls'

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

                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'auto_subs.wsgi.application'



if os.getenv('dockerenv'):
    
    print('Docker!!!')
    
    SITE_ID = 3
    DEBUG = os.environ.get('DEBUG')
    RESULT_HOST = os.environ.get('RESULT_HOST')

    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND')
    
    REDIS_HOST = os.environ.get('REDIS_HOST')
    REDIS_PORT = os.environ.get('REDIS_PORT')
    
    CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": os.environ.get('REDIS_URL'),
        }
    }
    
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get("DB_NAME"),
        'USER': os.environ.get("DB_USER"),
        'PASSWORD': os.environ.get("DB_PASSWORD"),
        'HOST': os.environ.get("DB_HOST"),
        'PORT': os.environ.get("DB_PORT"),
        }
    }



# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = (
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.vk.VKOAuth2',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.telegram.TelegramAuth',
    
    # 'allauth.account.auth_backends.AuthenticationBackend',
    
    'django.contrib.auth.backends.ModelBackend',
    'web_app_auto_subs.auth.EmailAuthBackend',
)

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.create_user',
    
    'web_app_auto_subs.social_auth_user_handler.new_user_handler',
    
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)


SOCIAL_AUTH_GITHUB_KEY = os.environ.get('SOCIAL_AUTH_GITHUB_KEY')
SOCIAL_AUTH_GITHUB_SECRET = os.environ.get('SOCIAL_AUTH_GITHUB_SECRET')


SOCIAL_AUTH_VK_OAUTH2_KEY = os.environ.get('SOCIAL_AUTH_VK_OAUTH2_KEY')
SOCIAL_AUTH_VK_OAUTH2_SECRET = os.environ.get('SOCIAL_AUTH_VK_OAUTH2_SECRET')
SOCIAL_AUTH_VK_OAUTH2_SCOPE = ['email']


SOCIAL_AUTH_GOOGLE_OAUTH2_KEY= os.environ.get('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ.get('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')
SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI = 'http://127.0.0.1:8000/social_auth/complete/google-oauth2/'


# SOCIAL_AUTH_TELEGRAM_KEY = os.environ.get('SOCIAL_AUTH_TELEGRAM_KEY')
# SOCIAL_AUTH_TELEGRAM_SECRET = os.environ.get('SOCIAL_AUTH_TELEGRAM_SECRET')


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

# LANGUAGE_CODE = 'ru-RU'
LANGUAGE_CODE = 'en-EN'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static'),
# ]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGIN_URL = 'login'
LOGOUT_REDIRECT_URL = 'main'
LOGIN_REDIRECT_URL = 'main'




PATH_FOR_SUBTITLES = str(BASE_DIR) + '/media/subtitles/'
PATH_FOR_VIDEO_WITH_SUBS = str(BASE_DIR) + '/media/video_with_subs/'
BASE_PATH_OF_VIDEO = str(BASE_DIR) + '/media/'
PATH_FOR_AUDIO = str(BASE_DIR) + '/media/records/'
PATH_FOR_VIDEOS = BASE_PATH_OF_VIDEO + 'videos/'

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.yandex.ru'
# EMAIL_USE_TLS = False
# EMAIL_PORT = 465
# EMAIL_USE_SSL = True
# EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_USE_SSL = False
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')


USE_ABS_API = False

API_KEY = '0b84aeb8d4284cae91713495d558c506'

API_URL = 'https://emailvalidation.abstractapi.com/v1/?api_key=' + API_KEY


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'main_format': {
            "format": "{asctime} - {levelname} - {module} - {filename}:{lineno} - {funcName} - {message}",
            "style": "{",
        },
        'detailed_format': {
            "format": "{asctime} - {levelname} - {module} - {filename}:{lineno} - {funcName} - {message}\n{exc_info}",
            "style": "{",
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'main_format',
        },
        'file': {
            'class': 'logging.FileHandler',
            'formatter': 'detailed_format',
            'filename': 'information.log',
        },
    },
    'loggers': {
        'main': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
        # 'django': {
        #     'handlers': ['console', 'file'],
        #     'level': 'ERROR',
        #     'propagate': True,
        # },
    },
}


logger = logging.getLogger('main')


CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Укажите домен, откуда будет происходить запрос
    "http://localhost:8000",
]

CORS_ALLOW_HEADERS = [
    'content-type',
]

CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'PUT',
    'DELETE',
    'OPTIONS',
]
