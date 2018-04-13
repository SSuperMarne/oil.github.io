from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.IntegerField(default=50)
    oil = models.IntegerField(default=0)
    avatar = models.ImageField(upload_to="avatars", blank=True)
    stat_tower = models.IntegerField(default=0)
    stat_produced = models.IntegerField(default=0)
    stat_pay = models.IntegerField(default=0)
    stat_payout = models.IntegerField(default=0)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Transfer(models.Model):
    @property
    def user(self):
        return User.objects.get(pk=self.user_id)
    amount = models.IntegerField()
    system = models.CharField(max_length=16)
    vault = models.CharField(max_length=64)
    date = models.DateTimeField(auto_now_add=True)
    user_id = models.IntegerField()
    # Статусы платежей: 1 - выплачено, 2 - отклонено, 3 - обработка
    status = models.IntegerField()

class ReferralSys(models.Model):
    @property
    def user(self):
        return User.objects.get(pk=self.id_referral)
    id_referral = models.IntegerField()
    id_referrer = models.IntegerField()
    profit = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)