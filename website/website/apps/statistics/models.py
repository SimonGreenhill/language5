from django.db import models

class StatisticalValue(models.Model):
    """Stores Statistical information"""
    date = models.DateTimeField(auto_now_add=True, db_index=True)
    label = models.CharField(max_length=128, db_index=True)
    model = models.CharField(max_length=255)
    method = models.CharField(max_length=12)
    field = models.CharField(max_length=32)
    value = models.FloatField()
    
    def __unicode__(self):
        return "%s = %s" % (self.label, self.value)
    
    class Meta:
        db_table = 'statistics'

