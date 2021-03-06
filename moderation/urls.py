from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^moderation/$', views.moderation, name='moderation'),
    url(r'^transfer/(?P<status>(accept|deny))/(?P<pk>\d+)/$', views.transfer_change, name='mod_wd'),
    url(r'^transfer/auto/(?P<pk>\d+)/$', views.transfer_auto, name='mod_wd_auto'),
    url(r'^moderation/do/(?P<action>(referrals|modify|statistic|inventory))/$', views.mod_actions, name='mod_act'),
    url(r'^moderation/email_list/$', views.get_emaillist, name='mod_email'),
]