from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^moderation/$', views.moderation, name='moderation'),
    url(r'^moderation/support/(?P<pk>\d+)/$', views.support_del, name='support_del'),
    url(r'^transfer/(?P<status>(accept|deny))/(?P<pk>\d+)/$', views.transfer_change),
]