from django.conf.urls import patterns, url

from booking import views

urlpatterns = patterns('',
    url(r'^(?P<room_id>\d+)/$', views.detail, name='detail'),
    url(r'^(?P<room_id>\d+)/create_event/$', views.create_event, name='create_event'),
    url(r'^view_event/(?P<event_id>\d+)/$', views.view_event, name='view_event')

)