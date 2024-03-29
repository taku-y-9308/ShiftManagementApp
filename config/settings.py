from pathlib import Path
import os
import dj_database_url



AUTH_USER_MODEL = 'ShiftManagementApp.User'

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

DEBUG = False

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
    'log': {
        '()': 'django.utils.log.ServerFormatter',
        'format': '[%(levelname)s]%(message)s',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'log'
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}


ALLOWED_HOSTS = ['127.0.0.1', '.herokuapp.com','shiftmanagementapp.com','localhost','gunicorn-django']
CSRF_TRUSTED_ORIGINS= ['shiftmanagementapp.com']

#Email settings
#AWS_ACCESS_KEY_ID = ""

#AWS_SECRET_ACCESS_KEY = ""

AWS_SES_REGION_NAME="ap-northeast-1"

AWS_SES_REGION_ENDPOINT="email.ap-northeast-1.amazonaws.com"

#EMAIL_BACKEND="django_ses.SESBackend"
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = 'no-reply@shiftmanagementapp.com'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Application definition

INSTALLED_APPS = [
    'ShiftManagementApp',
    'django_ses',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
#'django.middleware.csrf.CsrfViewMiddleware'を一時的に削除
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

#未ログインユーザーがログインが必要なページにアクセスした時のリダイレクト先
LOGIN_URL = "ShiftManagementApp:Login"

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
# dj_databases_urlを用いて、環境変数"DATABASE_URL"からdatabase設定を読み取る

DATABASES = {
    'default': dj_database_url.config(conn_max_age=600)
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

'''
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

'''


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),
]

#STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_ROOT = '/usr/share/nginx/html/static'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

try:
    from .local_settings import *
except ImportError:
    pass

if not DEBUG:
    SECRET_KEY = os.environ.get('SECRET_KEY')

    #heroku用の設定なので、PLATFORMが明示的にAWSとわかっている時は実行しない
    if os.environ.get('PLATFORM') != 'AWS':
        import django_heroku
        django_heroku.settings(locals(),databases=False)