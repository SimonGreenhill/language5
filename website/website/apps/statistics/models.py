from django.db import models
from django.utils.encoding import python_2_unicode_compatible

class AlreadyRegistered(Exception):
    pass


class InvalidField(Exception):
    pass


class InvalidMethod(Exception):
    pass


class Statistic(object):
    def __init__(self):
        self._registry = {}
        self._statistics = {
            'count': self._get_count,
        }
    
    def _get_count(self, model, field='id'):
        """Method to get the count of `field` from `model`"""
        if field != 'id':
            raise InvalidField("Expecting the field to be `id`")
        return model.objects.count()
        
    def get_statistic(self, label):
        model, field, method, graph = self._registry[label]
        return self._statistics[method](model, field)
    
    def update(self, save=True):
        out = {}
        for label in self._registry:
            value = self.get_statistic(label)
            out[label] = value
            if save:
                StatisticalValue.objects.create(
                    label=label,
                    model=self._registry[label][0].__module__,
                    field=self._registry[label][1],
                    method=self._registry[label][2],
                    value=value
                )
        return out
        
    def get_graphing(self):
        """Returns a list of the statistics to graph"""
        tograph = []
        for label in self._registry:
            if self._registry[label][-1] > 0:
                tograph.append((label, self._registry[label][-1]))
        return [_[0] for _ in sorted(tograph, key=lambda tup: tup[1])]
    
    def register(self, label, model, field='id', method="count", graph=False):
        """
        Registers the given model(s) with the given admin class.
        """
        if label in self._registry:
            raise AlreadyRegistered(
                'The model %s is already registered as %s' % (
                    model.__name__, label
                )
            )
        if method not in self._statistics:
            raise InvalidMethod(
                'Invalid statistical method `%s`. Valid values are: %s' % (
                    method, ",".join(self._statistics)
                )
            )
        # Instantiate the admin class to save in the registry
        self._registry[label] = (model, field, method, graph)


class StatisticManager(models.Manager):
    def get_all(self, label):
        qset = self.filter(label=label).values_list('value', flat=True)
        return qset.order_by('date')
    
    def get_all_with_dates(self, label):
        qset = self.filter(label=label).values_list('value', 'date')
        return qset.order_by('date')


@python_2_unicode_compatible
class StatisticalValue(models.Model):
    """Stores Statistical information"""
    date = models.DateTimeField(auto_now_add=True, db_index=True)
    label = models.CharField(max_length=128, db_index=True)
    model = models.CharField(max_length=255)
    method = models.CharField(max_length=12)
    field = models.CharField(max_length=32)
    value = models.FloatField()
    
    objects = StatisticManager()
    
    def __str__(self):
        return "%s = %s" % (self.label, self.value)
    
    class Meta:
        db_table = 'statistics'
        ordering = ['date', ]
        get_latest_by = 'date'
        app_label = 'statistics'
        

statistic = Statistic()
