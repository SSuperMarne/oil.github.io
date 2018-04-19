from django.db import models

class Tariff(models.Model):
    name = models.CharField(max_length=50, help_text="Название тарифа")
    color = models.BooleanField(help_text="Выделение цветом в общем списке")
    blank = models.BooleanField(help_text="Просмотр в активном окне")
    time = models.PositiveSmallIntegerField(help_text="Время просмотра сайта (сек.)")
    price = models.PositiveSmallIntegerField(help_text="Цена за 1000 просмотров (руб.)")

    def __str__(self):
        return self.name

class SurfingSite(models.Model):
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE)
    user_id = models.IntegerField()
    balance = models.FloatField()
    title = models.CharField(max_length=120)
    url = models.URLField()
    status = models.BooleanField()