from .production import *

# Development Settings

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

HANLIGHT_BASE_URL = 'https://test-backend.hanlight.kr/api/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Django Debug Toolbar Settings
INTERNAL_IPS = ('127.0.0.1', 'localhost', )
MIDDLEWARE += ('debug_toolbar.middleware.DebugToolbarMiddleware', )
INSTALLED_APPS += ('debug_toolbar', )
