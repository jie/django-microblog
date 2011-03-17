from django.conf.urls.defaults import *
from account.views import *
urlpatterns = patterns('',
  (r'^signup/$',  signup_view),
  (r'^login/$', login_view),
  (r'^logout/$', logout_view),
  (r'^(\w+)/$', member_view),
  (r'', self_view),
)