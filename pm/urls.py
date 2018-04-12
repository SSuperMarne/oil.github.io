from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^messages/$', views.pm_list, name='pm_list'),
    url(r'^messages/write/$', views.pm_new_create, name='pm_new_create'),
]