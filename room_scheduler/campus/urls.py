from django.conf.urls import patterns, url

from campus import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index')
)