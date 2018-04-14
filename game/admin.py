from django.contrib import admin
from .models import Statistic, Factory, Tower, Advertisement, TowerLevel

admin.site.register(Statistic)
admin.site.register(Factory)
admin.site.register(Tower)
admin.site.register(Advertisement)
admin.site.register(TowerLevel)