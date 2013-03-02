from django.conf.urls import patterns, include, url
from smartcode.views import home
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'engine.views.home', name='home'),
    # url(r'^engine/', include('engine.foo.urls')),
    url(r'^$', home, name='home'),
    url(r'^smartcode', include('smartcode.urls')),
    url(r'^accounts', include('accounts.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls))
)
