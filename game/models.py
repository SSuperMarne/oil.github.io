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

class Tower(models.Model):
    name = models.CharField(max_length=30, unique=True)
    oil = models.IntegerField()
    price = models.IntegerField()
    img = models.ImageField(upload_to='towers')

    def __str__(self):
        return self.name

class Factory(models.Model):
    name = models.CharField(max_length=30, unique=True)
    price = models.IntegerField()
    img = models.ImageField(upload_to='factories')
    tower_id = models.IntegerField()

    def __str__(self):
        return self.name

class ClientTower(models.Model):
    tower_id = models.ForeignKey(Tower, on_delete=models.CASCADE)
    user_id = models.IntegerField(blank=False)
    work = models.IntegerField()
    tower_name = models.CharField(max_length=256, blank=False)
    tower_oil = models.IntegerField(blank=False)

class ClientFactory(models.Model):
    factory = models.ForeignKey(Factory, on_delete=models.CASCADE)
    name = models.CharField(max_length=64, blank=False)
    user_id = models.IntegerField(blank=False)
    tower_id = models.IntegerField()