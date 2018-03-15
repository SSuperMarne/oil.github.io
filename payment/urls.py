from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^payment/$', views.add_payment, name='payment'),
    url(r'^payment/payeer/status/$', views.payeer_status),
    url(r'^payment/(?P<status>(success|fail))/$', views.payment_status),
]