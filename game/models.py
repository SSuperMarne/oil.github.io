from django.db import models

class Statistic(models.Model):
    tower = models.IntegerField()
    oil = models.IntegerField()
    donated = models.IntegerField()
    exchanged = models.IntegerField()