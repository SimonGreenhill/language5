from django.http import HttpResponse
from tastypie.resources import ModelResource

# sets default character type as UTF-8:
# https://stackoverflow.com/questions/17280513/tastypie-json-header-to-use-utf-8

def build_content_type(format, encoding='utf-8'):
    """
    Appends character encoding to the provided format if not already present.
    """
    if 'charset' in format:
        return format
    return "%s; charset=%s" % (format, encoding)

class UTF8ModelResource(ModelResource):
    def create_response(self, request, data, response_class=HttpResponse, **response_kwargs):
        """
        Extracts the common "which-format/serialize/return-response" cycle.
        
        Mostly a useful shortcut/hook.
        """
        desired_format = self.determine_format(request)
        serialized = self.serialize(request, data, desired_format)
        return response_class(
            content=serialized, 
            content_type=build_content_type(desired_format), 
            **response_kwargs
        )
        
