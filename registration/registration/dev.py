from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*']
SECRET_KEY = 'c-d$eym5#7%(l3*_t1@l6sgq_ts1h@6jq($1c-9g258y%9e=#u'

try:
    from .local import *
except ImportError:
    pass
