from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^account/$', views.panel_main, name='panel_main'),
    url(r'^statistic/$', views.panel_stats, name='statistic'),
    url(r'^support/$', views.new_support, name='support'),
    url(r'^exchange/$', views.exchange, name='exchange'),
    url(r'^shop/$', views.shop, name='shop'),
    url(r'^shop/(?P<category>\d+)/(?P<goods>\d+)/$', views.buy, name='buy'),
    url(r'^inventory/$', views.inventory, name='inventory'),
    url(r'^inventory/get/(?P<pk>\d+)/$', views.get_oil, name='get_oil'),
    url(r'^inventory/get/all/$', views.get_all_oil, name='get_all_oil'),
]