import os
from pathlib import Path
from decouple import config
from django.contrib.messages import constants as messages

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'error',
}

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-0kd*0gdxql5@*hzeg4%qjhq*oom9kla*u@6j5hs=6bo6-gne0h"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = ['https://bolao-virtual.onrender.com/']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bolao',
]

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

ROOT_URLCONF = 'core.urls'

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

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'bolao_virtual_db',
        'USER': 'admin',
        'PASSWORD': 'ZGUMLnWdRnoUy7JishE5EjYOmREE2dGv',
        'HOST': 'dpg-csdtpqbv2p9s73b1e1u0-a.oregon-postgres.render.com',
        'PORT': '5432',
    }
}


# Password validation postgresql://admin:ZGUMLnWdRnoUy7JishE5EjYOmREE2dGv@ dpg-csdtpqbv2p9s73b1e1u0-a/bolao_virtual_db
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'static/images')
MEDIA_URL = "imagens/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field     irnwrulapjpbpdgk

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


EMAIL_HOST = 'smtp.office365.com'  # Servidor SMTP do Outlook/Office 365
EMAIL_PORT = 587  # Porta para TLS
EMAIL_USE_TLS = True  # Ativa TLS para envio seguro
EMAIL_HOST_USER = 'hiaguinhospencer@outlook.com'  # Seu endereço de email do Outlook
EMAIL_HOST_PASSWORD = 'hjkguwfmyzzlapyy'  # Senha da conta do Outlook
DEFAULT_FROM_EMAIL = 'hiaguinhospencer@outlook.com'  # Remetente padrão

# codigo autenticacao 2 etapas microsoft  Q65LM-3EWVH-UCCEF-8DY9C-6ABE8

# DEFAULT_FROM_EMAIL = "hiaguinhospencer@gmail.com"
# EMAIL_HOST_USER = "hiaguinhospencer@gmail.com"
# EMAIL_HOST_PASSWORD = "lnai yjwo qtdv wuzc"
# EMAIL_USE_TSL = True
# EMAIL_PORT = 587
# EMAIL_HOST = "smtp.gmail.com"
