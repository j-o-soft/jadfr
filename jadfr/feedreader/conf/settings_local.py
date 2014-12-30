from feedreader.conf.base import Dev


class MyConf(Dev):
    DATABASES = {
        'default': {
            'NAME': 'jadfr',
            'USER': 'postgres',
            'PASSWORD': 's0melongTestingPaxssw0rd',
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'HOST': 'localhost'
        }
    }

    BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

