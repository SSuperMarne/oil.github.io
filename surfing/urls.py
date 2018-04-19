from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^surfing/add/$', views.surfing_add, name='add_surfing'),
]