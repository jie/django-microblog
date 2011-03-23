from django.conf.urls.defaults import *
from main.views import *

urlpatterns = patterns('',
  (r'^all/$', all_topics),
  (r'^me/$', me_topics),
  (r'^archieve/index/$', archieve_topics),
  (r'^people/(?P<people>\w+)/$', people_topics),
)
