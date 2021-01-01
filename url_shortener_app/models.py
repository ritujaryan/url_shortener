from django.db import models

# Create your models here.
class LongToShort(models.Model):
    longurl = models.URLField(max_length=250)
    shorturl = models.CharField(max_length=25, unique=True)
    visit_count = models.IntegerField(default = 1)

class UserLocation(models.Model):
    shorturl = models.CharField(max_length=25, unique=True)
    city = models.CharField(max_length=25)
    long = models.DecimalField(max_digits=8, decimal_places=3)
    lat = models.DecimalField(max_digits=8, decimal_places=3) 
