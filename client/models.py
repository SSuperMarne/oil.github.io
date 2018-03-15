from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0, blank=False)
    oil = models.IntegerField(default=0, blank=False)
    stat_tower = models.IntegerField(default=0, blank=False)
    stat_produced = models.IntegerField(default=0, blank=False)
    stat_pay = models.IntegerField(default=0, blank=False)
    stat_payout = models.IntegerField(default=0, blank=False)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()