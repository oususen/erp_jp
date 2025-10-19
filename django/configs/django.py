from pathlib import Path


# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'USER': 'erp_user',
        'PASSWORD': 'daisofutu1470-3',
        'NAME': 'erp_db',
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}
