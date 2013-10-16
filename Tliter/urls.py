from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'twitter.views.index'),
    url(r'tweets/', include('twitter.urls', namespace='twitter')),
    url(r'logout/', 'twitter.views.logout', name='logout'),
    url(r'login/', 'twitter.views.login', name='login'),
)