from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^messages/$', views.pm_list, name='pm_list'),
    url(r'^messages/write/$', views.pm_new_create, name='pm_new_create'),
    url(r'^messages/view/(?P<pk>\d+)/$', views.pm_view, name='pm_view'),
    url(r'^messages/delete/(?P<pk>\d+)/$', views.pm_delete, name='pm_delete'),
    url(r'^support/$', views.pm_support_new, name='pm_support_new'),
    url(r'^support/view/(?P<pk>\d+)/$', views.pm_support_view, name='pm_support_view'),
]