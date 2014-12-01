def expire_view_cache(view_name, args=[], namespace=None, key_prefix=None, method="GET"):
    """
    This function allows you to invalidate any view-level cache. 
        view_name: view function you wish to invalidate or it's named url pattern
        args: any arguments passed to the view function
        namespace: optional, if an application namespace is needed
        key prefix: for the @cache_page decorator for the function (if any)

        from: http://stackoverflow.com/questions/2268417/expire-a-view-cache-in-django
        added: method to request to get the key generating properly
    """
    import logging
    from django.core.urlresolvers import reverse
    from django.http import HttpRequest
    from django.utils.cache import get_cache_key
    from django.core.cache import cache

    logger = logging.getLogger("utilities.expire_view_cache")
    
    # create a fake request object
    request = HttpRequest()
    request.method = method
    # Loookup the request path:
    if namespace:
        view_name = namespace + ":" + view_name
    request.path = reverse(view_name, args=args)
    # get cache key, expire if the cached item exists:
    key = get_cache_key(request, key_prefix=key_prefix)
    if key:
        if cache.get(key):
            cache.set(key, None, 0)
            logger.info("Overriding cache for %s" % key)
        return True
    logger.info("No cache for %s" % key)
    return False


