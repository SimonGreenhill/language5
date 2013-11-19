Django Configuration
====================

General settings go into "base.py". 

Local environment overrides etc go into "local.py". This file is NOT under
revision control and needs to be written specifically for each environment.


In Production
-------------

1. Consider adding a cache:

	CACHES = {
	    'default': {
	        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
	        #'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
	        'LOCATION': 'cache',
	    }
	}

	And to middleware:
	
	'django.middleware.cache.UpdateCacheMiddleware', # first in sequence!
	# ... other middle
	#    'django.middleware.cache.FetchFromCacheMiddleware',
	