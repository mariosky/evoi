from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Collection(models.Model):
    V_TYPE = (
        (u'PR', u'Private'),
        (u'PU', u'Public'),
        )
    name = models.CharField(max_length=50)
    description = models.TextField()
    creation_date = models.DateTimeField()
    visibility = models.CharField(max_length=16, choices=V_TYPE)
    users = models.ManyToManyField(User, through='User_Collection')

    def __unicode__(self):
        return u'%s %s' % (self.name, self.description)


class User_Collection(models.Model):
    STATUS_TYPE= (
        (u'PR', u'Private'),
        (u'PU', u'Public')
        )
    ROLE_TYPE=(
        (u'O', u'Owner'),
        (u'C', u'Collaborator'),
        (u'A', u'Anonymous')
        )
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    collection = models.ForeignKey(Collection,on_delete=models.CASCADE)
    role = models.CharField(max_length=45, choices=ROLE_TYPE)
    status = models.CharField(max_length=45, choices=STATUS_TYPE)


class Collection_Individual(models.Model):
    collection = models.ForeignKey(Collection, related_name='individuals', on_delete=models.CASCADE)
    individual_id = models.CharField(max_length=60)
    added_from = models.ForeignKey(Collection, null=True, on_delete=models.SET_NULL)
    from_user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    date_added = models.DateTimeField()
