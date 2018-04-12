from django.db import models
from django.contrib.auth.models import User

class Ticket(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    recipient = models.IntegerField(default=0)
    title = models.CharField(max_length=120)
    # status: 0 - correspondence | 1 - closed 2 - opened 3 - wait (technical support)
    status = models.PositiveSmallIntegerField(default=0)
    @property
    def recipient_name(self):
        return User.objects.get(pk=self.recipient)

class PersonalMessage(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    message = models.TextField(max_length=3000)
    # True - owner, False - responser
    status = models.BooleanField()