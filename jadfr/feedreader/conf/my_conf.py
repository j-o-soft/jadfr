from feedreader.conf.base import Dev, Test


class MyConf(Dev):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'jadfr',
            'USER': 'postgres',
            'PASSWORD': 's0melongTestingPassw0rd',
            'HOST': 'localhost'
        }
    }

    BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'


class MyTestConf(Test):
    pass
