from .base import * 

DEBUG = TEMPLATE_DEBUG = False

MIDDLEWARE_CLASSES.extend([
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',

    # Remove this once live
    'website.apps.core.middleware.LoginRequiredMiddleware',

])
