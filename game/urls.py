from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^account/$', views.panel_main, name='panel_main'),
    url(r'^statistic/$', views.panel_stats, name='statistic'),
    url(r'^support/$', views.new_support, name='support'),
]