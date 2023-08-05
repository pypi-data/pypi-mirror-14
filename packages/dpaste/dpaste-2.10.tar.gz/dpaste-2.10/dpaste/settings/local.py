from dpaste.settings.base import *

DEBUG = True

ADMINS = (
    #('Your Name', 'name@example.com'),
)
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dpaste',
        'USER': 'martin',
        'PASSWORD': '',
    }
}

SECRET_KEY = 'changeme'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
