from django.conf.urls.defaults import *
from mail.views import *


urlpatterns = patterns('',
  (r'^generic/inbox/$', inbox_generic_view),
  (r'^generic/sendbox/$', sendbox_generic_view),
  (r'^generic/delete/(\d+)/', delete_mail_generic_view),
  (r'^mailto/(\d+)/$', mail_view),
  (r'^inbox/$', inbox_view),
  (r'^sendbox/$', sendbox_view),
  (r'^delete/(\d+)/', delete_mail),
)