from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.


class Collection(models.Model):
    V_TYPE = (
        (u'PR', u'Private'),
        (u'PU', u'Public'),
        )
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    creation_date = models.DateTimeField(default=datetime.now)
    visibility = models.CharField(max_length=16, choices=V_TYPE)
    owner = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __unicode__(self):
        return u'%s %s' % (self.name, self.description)


class Collection_Individual(models.Model):
    collection = models.ForeignKey(Collection, related_name='individuals', on_delete=models.CASCADE)
    individual_id = models.CharField(max_length=60)
    added_from = models.ForeignKey(Collection, null=True, on_delete=models.SET_NULL)
    from_user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    date_added = models.DateTimeField(default=datetime.now)
