from django.conf import settings
from django.test.runner import DiscoverRunner, reorder_suite

class InstalledAppsRunner(DiscoverRunner):
    def build_suite(self, test_labels=None, extra_tests=None, **kwargs):
        if test_labels is None or len(test_labels) == 0:
            test_labels = [app for app in settings.INSTALLED_APPS if app.startswith("website")]
        else:
            test_labels = ['.']
            
        suite = super(InstalledAppsRunner,self).build_suite(test_labels)
        return reorder_suite(suite, self.reorder_by)
        