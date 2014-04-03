from django.db import models

# Create your models here.
class Location(TrackedModel):
    language = models.ForeignKey('website.apps.core.Language')
    longitude = models.FloatField(help_text="Longitude")
    latitude = models.FloatField(help_text="Latitiude")

    def __unicode__(self):
        return "%d %2.4f-%2.4f" % (self.language.id, self.longitude, self.latitude)

    class Meta:
        verbose_name_plural = "Geographical Locations"
        db_table = 'locations'

