import os

DEBUG = True

LOCAL_SETTINGS = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'EXAMPLE_PERSONAL_SERVICES',
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': 'db',
    }
}


SBERBANK_SBBOL_URL = "https://edupir.testsbi.sberbank.ru:9443"

PASSPORT_URL = "https://passport.example.tyu"
PASSPORT_URL_REDIRECT = "https://passport.example.tyu"
