from django.conf.urls import patterns, url

from twitter import views

urlpatterns = patterns('',
    url(r'^(?P<tweet_id>\d+)/$', views.show_tweet, name='show_tweet'),
    url(r'^$', views.index, name='index'),
)