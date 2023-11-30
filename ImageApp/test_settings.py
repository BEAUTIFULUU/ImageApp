from .settings import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'test_tb',
        'USER': 'test_user',
        'PASSWORD': 'test_password',
        'HOST': 'db',
        'PORT': '5432',
    }
}
