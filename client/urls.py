from django.conf.urls import url
from django.contrib.auth import views as auth_views
from .forms import LPasswordForm
from . import views

urlpatterns = [
# registration URLs
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/login/'}, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^reg/(?P<referrer>\d+)/$', views.referral, name='refreg'),
    url(r'^password_reset/$', auth_views.password_reset, {'template_name': 'registration/passwd_reset_form.html', 
        'email_template_name': 'registration/passwd_reset_email.html', 'password_reset_form': LPasswordForm}, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, {'template_name': 'registration/passwd_reset_done.html'}, 
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, {'template_name': 'registration/passwd_reset_confirm.html'}, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, {'template_name': 'registration/passwd_reset_complete.html'}, name='password_reset_complete'),
    url(r'^profile/passwd/$', auth_views.PasswordChangeView.as_view(template_name='registration/passwd.html'), name='passwd'),
    url(r'^profile/passwd/done/$', auth_views.password_change_done, {'template_name': 'registration/passwd.html'}, name='password_change_done'),
# other client urls
    url(r'^profile/$', views.u_profile, name='profile'),
    url(r'^profile/avatar/$', views.u_avatar, name='avatar'),
    url(r'^payment/history/$', views.payment_history, name='payment_history'),
    url(r'^withdraw/$', views.transfer, name='withdraw'),
    url(r'^payment/(?P<pk>\d+)/(?P<action>[a-z]+)/$', views.payment_manage, name='payment_manage'),
]