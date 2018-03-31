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

class Promotion(models.Model):
    name = models.CharField(max_length=64, unique=True, help_text="Укажите название акции. Оно будет видно только вам.")
    description = models.TextField(help_text="Система будет отображать этот текст пользователям при пополнении счёта. HTML-коды разрешены.")
    promo = models.PositiveSmallIntegerField(help_text="Бонус при пополнении в процентах")

    def __str__(self):
        return self.name