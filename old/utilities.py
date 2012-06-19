"Misc Utilies."

def ensure_unicode(fn):
    """
    Decorator to ensure unicode arguments
    """
    def map_value(x):
        return (x if not isinstance(x, str) else unicode(x, encoding="utf-8"))
        
    def wrapper(*args, **kwargs):
        neo_args = [map_value(x) for x in args]
        neo_kwargs = dict([(k, map_value(v)) for k,v in kwargs.items()])
        return fn(*neo_args, **neo_kwargs)
        
    wrapper.__name__ = fn.__name__
    wrapper.__dict__ = fn.__dict__
    wrapper.__doc__ = fn.__doc__
    return wrapper
