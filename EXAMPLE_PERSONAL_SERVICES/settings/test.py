import os

DEBUG = True

ALLOWED_HOSTS = ['personal.back.example.tyu']

LOCAL_SETTINGS = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'EXAMPLE_PERSONAL_SERVICES',
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': 'db',
    }
}

API_1C_URL = "https://1ctest.example.tyu"
API_1C_BASE = "erp_base"
API_1C_BASE_ECM = "ecm"

TRACKING_TOKEN = os.environ['TRACKING_TOKEN']
TRACKING_DOMAIN = 'https://personal.example.tyu'

PASSPORT_URL = "https://passport.example.tyu"

CREDIT_REDIRECT_URN = "/bank_account/credit_redirect"
UNLINK_REDIRECT_URN = "/bank_account/unlink_redirect"