from django.conf.urls.defaults import *
from oauth_lib.views import douban_login, douban_logout, douban_authenticated

urlpatterns = patterns('',
  (r'^login/?$', douban_login),
  (r'^logout/?$', douban_logout),
  (r'^login/authenticated/?$', douban_authenticated),
)