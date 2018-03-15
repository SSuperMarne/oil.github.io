from django.db import models

class Order(models.Model):
    amount = models.IntegerField()
    user_id = models.IntegerField()
    status = models.BooleanField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id