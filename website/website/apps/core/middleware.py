from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse, resolve
from django.http import HttpResponseRedirect

class LoginRequiredMiddleware:
    """
    Middleware that requires a user to be authenticated to view any page other
    than /admin/
    """
    
    def process_request(self, request):
        if not hasattr(request, 'user'):
            raise ImproperlyConfigured("""
            Please ensure that 
            1. 'django.contrib.auth.middlware.AuthenticationMiddleware' is in
                    MIDDLEWARE_CLASSES
            2. 'django.core.context_processors.auth' is in
                    TEMPLATE_CONTEXT_PROCESSORS
            """)
        
        # if we're not authenticated...
        if not request.user.is_authenticated():
            url = resolve(request.path_info)
            # and not trying to load an admin URL...
            if not url.namespace == 'admin':
                # go to login view.
                return HttpResponseRedirect(reverse("admin:index"))
