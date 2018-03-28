DEBUG = False
ALLOWED_HOSTS = ['oil-game.win', 'www.oil-game.win']
ADMINS = [('Dmitry', 'd@dmitry.win')]
MANAGERS = ADMINS

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'example_secret_key'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test_pipelines',
        'USER': 'test_user',
        'PASSWORD': 'test_user_password',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'sql_mode': 'traditional',
        },
        # ONLY TEST MODE #
        'TEST': {
            'NAME': 'test_pipelines',
            'CHARSET': 'UTF8',
        },
        # END ONLY TEST MODE #
    }
}

#CACHES = {
#    'default': {
#        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#        'LOCATION': '127.0.0.1:11211',
#    }
#}

## Mail settings ##
# FILE # 
#EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
#EMAIL_FILE_PATH = 'tmp/'

# SMTP # 
SERVER_EMAIL = 'robot@oil-game.win'
DEFAULT_FROM_EMAIL = 'robot@oil-game.win'
EMAIL_HOST_USER = 'robot@oil-game.win'
EMAIL_HOST_PASSWORD = ''

EMAIL_SUBJECT_PREFIX = ''
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = '465'
EMAIL_BACKENDS = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_SSL = True
## End mail settings ##

# Recaptcha
RECAPTCHA_PUBLIC_KEY = ''
RECAPTCHA_PRIVATE_KEY = ''
NOCAPTCHA = True