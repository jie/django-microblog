from posts import views
from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'/create_image/(.*)/$', views.create_qrcode_view, name='create_qrcode_view'),
                       url(r'/create$', views.create_post_view, name='create_post_view'),
                       url(r'/all', views.posts_list_view, name='posts_list_view'),
                       url(r'/detail/(.*)', views.post_detail_view, name='post_detail_view'),
                       url(r'/qrcode_image/(.*)/$', views.qrcode_image_view, name='qrcode_image_view')
                       )
