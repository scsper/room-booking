from django.conf.urls import patterns, url

from campus import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^attributes/$', views.attributes, name='attributes'),
    url(r'^search/$', views.search, name='search')
)