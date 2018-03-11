from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.landing_main, name='landing_main'),
]