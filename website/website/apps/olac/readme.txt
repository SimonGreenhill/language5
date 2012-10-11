OLAC
====

1. Add context processor to TEMPLATE_CONTEXT_PROCESSORS in settings.py:
    olac.context_processors.InjectOLACSettings
    
    TEMPLATE_CONTEXT_PROCESSORS = (
        ...
        "website.apps.olac.context_processors.InjectOLACSettings",
    )

2. Add Settings to OLAC_SETTINGS in settings.py:
    These four settings are required at a minimum:
    
    # Setup OLAC
    from website.apps.olac.settings import OLAC_SETTINGS
    OLAC_SETTINGS['institution'] = 'My Institution'
    OLAC_SETTINGS['institutionURL'] = 'http://example.com'
    OLAC_SETTINGS['shortLocation'] = 'Some, Where'
    OLAC_SETTINGS['description'] = 'A great site'

3. If you are not using the Sites framework, make sure to have the two extra
    settings:
    
    OLAC_SETTINGS['sitename'] = 'A great site'
    OLAC_SETTINGS['sitedomain'] = 'example.com
    