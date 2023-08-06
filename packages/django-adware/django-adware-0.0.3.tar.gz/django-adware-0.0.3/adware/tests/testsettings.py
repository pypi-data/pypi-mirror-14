DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}
SECRET_KEY = "un33k"
MIDDLEWARE_CLASSES = []

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'adware',
)

ADWARE_IMPRESSION_REWARD_ENABLED = True
ADWARE_DEFAULT_AD_CLIENT = 'ca-pub-905269603332983333'
ADWARE_DEFAULT_AD_SLOT = '3864455333'
