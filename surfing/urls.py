from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^surfing/add/$', views.surfing_add, name='add_surfing'),
    url(r'^surfing/edit/(?P<pk>\d+)/$', views.surfing_edit, name='edit_surfing'),
    url(r'^surfing/$', views.surfing_list, name='list_surfing'),
    url(r'^surfing/(?P<pk>\d+)/$', views.surfing, name='surfing'),
    url(r'^surfing/status/$', views.status, name='status_surfing'),
]