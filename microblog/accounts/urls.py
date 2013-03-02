from accounts import views
from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^/login$', views.login_view, name='login_view'),
    url(r'^/logout$', views.logout_view, name='logout_view'),
    url(r'^/settings$', views.settings_view, name='settings_view'),
    url(r'^/oauth2/weibo/authorize$', views.authorize_view, name='authorize_view'),
)
