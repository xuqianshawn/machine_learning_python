from django.db import models

# Create your models here.
class Runner(models.Model):
    name = models.CharField(max_length=200)
    lat = models.FloatField(default=0.0)
    lon = models.FloatField(default=0.0)
    type=models.IntegerField(default=0)
    weight=models.FloatField(default=0.0)
    height=models.FloatField(default=0.0)
    gender = models.CharField(max_length=10)
    averageSpeed=models.FloatField(default=0.0)
    averageDistance=models.FloatField(default=0.0)
    averageSinuosity=models.FloatField(default=0.0)