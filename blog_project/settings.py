"""
Django settings for blog_project project.

Generated by 'django-admin startproject' using Django 4.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
from dotenv import load_dotenv
import os
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

#static files


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('secret_key')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*"]

SITE_ID = 1

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    # 'django.contrib.sites', # must
    # 'allauth', # must
    # 'allauth.account', # must
    # 'allauth.socialaccount', # must
    # 'allauth.socialaccount.providers.google', # new
    'authentication',
    'pages',
    'user_profile',
    'article',
    # 'django_summernote',
    'taggit',
    'django.contrib.sitemaps',

    # # 'tailwind' setup
    # 'tailwind', # from the django-tailwind library
    # 'theme', # from inbuilt app, create by the 'python manage.py tailwind init' after enter app name
]

# # tailwind css framework register
# TAILWIND_APP_NAME = 'theme'
# # after this run the commend following 'python manage.py tailwind install' for all required dependency to install

# AUTHENTICATION_BACKENDS = [
#     # Needed to login by username in Django admin, regardless of `allauth`
#     'django.contrib.auth.backends.ModelBackend',

#     # `allauth` specific authentication methods, such as login by e-mail
#     'allauth.account.auth_backends.AuthenticationBackend',
# ]
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
   # 'social_django.middleware.SocialAuthExceptionMiddleware',

]

AUTH_USER_MODEL = 'authentication.User'

ROOT_URLCONF = 'blog_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
               # 'social_django.context_processors.backends',

            ],
        },
    },
]

WSGI_APPLICATION = 'blog_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'blog.db'),
    }
}

#DATABASES = {
 #'default': {
  #'ENGINE': 'django.db.backends.postgresql',
   #'NAME': os.environ.get('DB_NAME'),
   #'HOST': os.environ.get('DB_HOST'),
    #'PORT': os.environ.get('DB_PORT'),
   # 'USER': os.environ.get('DB_USER'),
  #  'PASSWORD': os.environ.get('DB_PASSWORD'),
 # }
#}

# 'OPTIONS': {'ssl': {'ca': os.environ.get('MYSQL_ATTR_SSL_CA')}}
# Finally got it working. the value for the OPTIONS key should be {'ssl': {'ssl-ca': env('MYSQL_ATTR_SSL_CA')}}
#I've had the same problem, and even when my columns are set to utf8mb4, it was still failing to save things like certain emoji characters. Turns out, Django was not using the same character set when connecting to the database. To solve this, you can specify a new OPTIONS entry in the Django DATABASES setting, telling it which charset to use:

#DATABASES = {
 #   'default': {
  #      'ENGINE': 'django.db.backends.mysql',
   #     'USER': 'xxxxx',
    #    'PASSWORD': 'xxxxx',
     #   'HOST': 'localhost',
      #  'OPTIONS': {
       #     'charset': 'utf8mb4',  # <--- Use this
        #}
    #}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
# MEDIA_URL = "media/"
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_SUCCESS_URL = 'home'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.console.EmailBackend'

CSRF_TRUSTED_ORIGINS = ["http://*.railway.app","https://markblogs-production.up.railway.app"]


CORS_ORIGIN_ALLOW_ALL= True
CORS_ALLOW_CREDENTIALS = True

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get("host_mail")
EMAIL_HOST_PASSWORD  = os.environ.get("host_mail_password")

LOGIN_URL = 'auth:signup'
LOGIN_REDIRECT_URL = 'pages:home'
LOGOUT_URL = 'auth:logout'
LOGOUT_REDIRECT_URL = 'pages:home'
#SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ""
#SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ""
# print(os.system("ls"))
