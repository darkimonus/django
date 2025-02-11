import os
from pathlib import Path


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = os.getenv("DEBUG", True)

ALLOWED_HOSTS = []


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mainapp.apps.MainappConfig',
    'django.contrib.sites',
    'posts',
    'profiles',
    'channels',
    'chats',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Allauth settings
SITE_ID = os.getenv("SITE_ID", default="1")

ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = os.getenv("ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS", default=3)
ACCOUNT_EMAIL_VERIFICATION = os.getenv("ACCOUNT_EMAIL_VERIFICATION", default='mandatory')
ACCOUNT_USERNAME_MIN_LENGTH = os.getenv("ACCOUNT_USERNAME_MIN_LENGTH", default=3)
ACCOUNT_AUTHENTICATION_METHOD = os.getenv("ACCOUNT_AUTHENTICATION_METHOD", default='username')
ACCOUNT_EMAIL_REQUIRED = os.getenv("ACCOUNT_EMAIL_REQUIRED", default=True)
ACCOUNT_EMAIL_UNIQUE = os.getenv("ACCOUNT_EMAIL_UNIQUE", default=True)

EMAIL_BACKEND = os.getenv("EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend")
EMAIL_HOST = os.getenv("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = os.getenv("EMAIL_PORT", default=587)
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", default=False)
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")


ACCOUNT_LOGIN_ATTEMPTS_LIMIT = os.getenv("ACCOUNT_LOGIN_ATTEMPTS_LIMIT", default=3)
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = os.getenv("ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT", default=300)


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "allauth.account.middleware.AccountMiddleware",
    'django_htmx.middleware.HtmxMiddleware',
]

ROOT_URLCONF = 'network.urls'

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
                'profiles.context_processors.profile_pic',
                'profiles.context_processors.invitations_received_no',
            ],
        },
    },
]

WSGI_APPLICATION = 'network.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': POSTGRES_DB,
        'USER': POSTGRES_USER,
        'PASSWORD': POSTGRES_PASSWORD,
        'HOST': POSTGRES_HOST,
        'PORT': POSTGRES_PORT,
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'EMAIL_AUTHENTICATION': True,
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    },
}

# LOGIN_URL = '/admin/'
LOGIN_REDIRECT_URL = '/posts'

STATICFILES_DIRS = [
    BASE_DIR / 'static_project'
]

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_cdn", "static_root")
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_cdn", "media_root")

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ASGI_APPLICATION = 'network.asgi.application'

# Run Celery in sync mode (for local development)
CELERY_WORK_SYNC = os.getenv("CELERY_WORK_SYNC")
CELERY_ALWAYS_EAGER = CELERY_WORK_SYNC is not None
CELERY_TASK_ALWAYS_EAGER = CELERY_WORK_SYNC is not None

# Celery via Redis (from environment variables)
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_DEFAULT_QUEUE = 'network_queue'
CELERY_BROKER_TRANSPORT_OPTIONS = {'queue_prefix': 'network_'}

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT", default=6379)
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

if REDIS_PASSWORD:
    REDIS_PATH = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/2"
    CHANNEL_REDIS_HOST = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/2"
else:
    REDIS_PATH = f"redis://{REDIS_HOST}:{REDIS_PORT}/2"
    CHANNEL_REDIS_HOST = (REDIS_HOST, REDIS_PORT)


CELERY_BROKER_URL = REDIS_PATH
CELERY_RESULT_BACKEND = REDIS_PATH
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": REDIS_PATH,
    }
}
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [CHANNEL_REDIS_HOST],
        },
    },
}
