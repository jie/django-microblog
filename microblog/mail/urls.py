from django.conf.urls.defaults import *
from mail.views import *
urlpatterns = patterns('',
  (r'^mailto/(\d+)/$', mail_view),
  (r'^inbox/$', inbox_view),
  (r'^sendbox/$', sendbox_view),
)

