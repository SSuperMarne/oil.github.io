from django.db import models
from django.contrib.auth.models import User

class Ticket(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    recipient = models.IntegerField(default=0)
    title = models.CharField(max_length=120)
    # status: 0 - correspondence | 1 - closed 2 - opened 3 - wait (technical support)
    status = models.PositiveSmallIntegerField(default=0)

class PersonalMessage(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    message = models.TextField(max_length=3000)