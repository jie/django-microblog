from django.conf.urls.defaults import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib.auth.decorators import login_required
from django.contrib import admin
from backend.views import *
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^microblog/', include('microblog.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    (r'^mail/', include('microblog.mail.urls')),
    (r'^member/signup/$',  signup_view),
    (r'^member/login/$', login_view),
    (r'^member/logout/$', logout_view),
    (r'^settings/$', settings_view),
    (r'^member/(\w+)/$', member_view),
    (r'^member/$', self_view),
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
