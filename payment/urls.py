from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^payment/$', views.add_payment, name='payment'),
]