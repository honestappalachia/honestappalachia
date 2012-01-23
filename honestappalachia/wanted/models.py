from django.db import models

# Create your models here.

class Story(models.Model):
    '''
    A text description and associated location
    '''
    description = models.CharField(max_length=140)
    location = models.CharField(max_length=140)

    lat = models.FloatField(editable=False)
    lng = models.FloatField(editable=False)
    created = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=True)

    def __unicode__(self):
        return u'%s%s' % (self.description[:20], "...")

    class Meta:
        verbose_name_plural = "stories"
