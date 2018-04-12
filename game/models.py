from django.db import models

class Statistic(models.Model):
    tower = models.IntegerField(help_text="Всего построенных вышек")
    oil = models.IntegerField(help_text="Всего единиц нефти добыто")
    donated = models.IntegerField(help_text="Всего внесено в проект (руб.)")
    exchanged = models.IntegerField(help_text="Всего выведено средств (руб.)")

class Tower(models.Model):
    name = models.CharField(max_length=30, unique=True, help_text="Укажите название вышки")
    oil = models.IntegerField(help_text="Производительность нефти в 24 часа (укажите число)")
    price = models.IntegerField(help_text="Цена за 1 шт. (укажите число)")
    img = models.ImageField(upload_to='towers', help_text="Изображение вышки")

    def __str__(self):
        return self.name

class Factory(models.Model):
    name = models.CharField(max_length=30, unique=True, help_text="Укажите название завода")
    price = models.IntegerField(help_text="Цена за 1 шт. (укажите число)")
    img = models.ImageField(upload_to='factories', help_text="Изображение завода")
    tower_id = models.IntegerField(help_text="Идентификатор связанной вышки в БД")

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

class Advertisement(models.Model):
    name = models.CharField(max_length=64, unique=True, help_text="Укажите название баннера. Оно будет видно только вам.")
    url = models.URLField(blank=False, help_text="Укажите URL-адрес, куда будет перенаправлять баннер после клика.")
    img = models.ImageField(upload_to='banners', help_text="Загрузите изображение баннера")

    def __str__(self):
        return self.name