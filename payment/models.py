from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
    @property
    def user(self):
        return User.objects.get(pk=self.user_id)
    amount = models.IntegerField()
    user_id = models.IntegerField()
    status = models.BooleanField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id