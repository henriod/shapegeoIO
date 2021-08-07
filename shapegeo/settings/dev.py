from .base import *

DEBUG = True

SECRET_KEY = os.getenv('SECRET_KEY', default='xa(y-$)wm89u*by9f!v@8b3o&7c!&8nt_rtp%yhk&)wtic62n7')

# Static files (CSS, JavaScript, Images)

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_TIMEOUT = 5

# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = str(BASE_DIR / 'staticfiles')

MEDIA_ROOT = str(BASE_DIR / 'media')
MEDIA_URL = '/media/'
