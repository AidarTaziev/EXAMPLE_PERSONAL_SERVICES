import os

DEBUG = False

LOCAL_SETTINGS = False


ALLOWED_HOSTS = ['personal.back.example.tyu']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'EXAMPLE_PERSONAL_SERVICES',
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': 'db',
    }
}


PASSPORT_URL = "https://passport.example.tyu"
PASSPORT_URL_REDIRECT = "https://passport.example.tyu"


# PASSPORT
# ===============================
PASSPORT_SECRET_KEY = os.environ['PASSPORT_SECRET_KEY']
PASSPORT_SESSION_ID_NAME = "passport_session_id"
MAIN_DOMAIN = 'example.tyu'
APP_SUBDOMAIN = 'reference.{0}'.format(MAIN_DOMAIN)
PASSPORT_USER_CREDENTIALS_URI = 'https://passport.example.tyu/auth/data'.format(MAIN_DOMAIN)
# ===============================

CREDIT_REDIRECT_URN = "/bank_account/credit_redirect"
UNLINK_REDIRECT_URN = "/bank_account/unlink_redirect"