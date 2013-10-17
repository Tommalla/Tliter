from django.conf.urls import patterns, url

from twitter import views

urlpatterns = patterns('',
    url(r'^(?P<tweet_id>\d+)/$', views.show_tweet, name='show_tweet'),
    url(r'^by/(?P<username>\w+)/$', views.tweets_by, name='tweets_by'),
    url(r'^add/$', views.add, name='add'),
    url(r'^$', views.index, name='index'),
)