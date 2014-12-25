from feedreader.conf.base import Dev, Test


class MyConf(Dev):
    DATABASES = {
        'default': {
            'NAME': 'jadfr',
            'USER': 'postgres',
            'PASSWORD': 's0melongTestingPassw0rd',
            'HOST': 'localhost'
        }
    }

    BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'


class MyTestConf(Test):
    INSTALLED_APPS = Test.INSTALLED_APPS + ['django_behave']
    TEST_RUNNER = 'django_behave.runner.DjangoBehaveTestSuiteRunner'