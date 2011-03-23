from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import admin
from backend.views import *
admin.autodiscover()

urlpatterns = patterns('',
  (r'^oauth/', include('oauth_lib.urls')),
  (r'^i18n/', include('django.conf.urls.i18n')),
  (r'^admin/doc/', include('django.contrib.admindocs.urls')),
  (r'^mail/', include('microblog.mail.urls')),
  (r'^passport/', include('microblog.account.urls')),
  (r'^topic/', include('microblog.main.urls')),
  (r'^member/(\w+)/$', member_view),
  (r'^member/$', self_view),
  (r'^settings/$', settings_view),
  (r'^post/$', post_topic),
  (r'^delete/$', delete_topic),
  (r'^follow/$', follow_member),
  (r'^fav/$', setfav_view),
  (r'^favorite/$', favorite_view),
  (r'^conversation/$', post_conversation),
  (r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),
  (r'^admin/', include(admin.site.urls)),
  (r'^$', index),
)
