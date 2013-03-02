import smartcode.views
from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^$', smartcode.views.create_smartcode_view,
                           name='create_smartcode_view'),
                       url(r'/create_post$', smartcode.views.create_post_view,
                           name='create_post_view'),
                       url(r'/posts', smartcode.views.posts_list_view,
                           name='posts_list_view'),
                       url(r'/post/detail/(.*)', smartcode.views.post_detail_view,
                           name='post_detail_view')
                       )
