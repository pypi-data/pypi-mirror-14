import os, sys
DEBUG = True
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SECRET_KEY = 'fake-key'
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'tests',
    'simple_email_verification'
]

ROOT_URLCONF = 'tests.urls'

EMAIL_HOST = 'your.mailserver.tld'

SIMPLE_EMAIL_VERIFICATION = {
    'EMAIL_FROM_ADDRESS': 'donotreply@domain.tld'
}

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'test.db.sqlite3'),
    }
}
