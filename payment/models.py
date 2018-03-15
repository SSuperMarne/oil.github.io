from django.db import models

class Order(models.Model):
    amount = models.IntegerField()
    user_id = models.IntegerField()
    status = models.BooleanField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id

class Transfer(models.Model):
    amount = models.IntegerField()
    system = models.CharField(max_length=16)
    vault = models.CharField(max_length=64)
    date = models.DateTimeField(auto_now_add=True)
    user_id = models.IntegerField()
    status = models.IntegerField()