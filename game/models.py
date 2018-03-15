from django.db import models

class Statistic(models.Model):
    tower = models.IntegerField()
    oil = models.IntegerField()
    donated = models.IntegerField()
    exchanged = models.IntegerField()

class Support(models.Model):
    nickname = models.CharField(max_length=150)
    email = models.EmailField()
    title = models.CharField(max_length=128)
    text = models.TextField(max_length=2048)