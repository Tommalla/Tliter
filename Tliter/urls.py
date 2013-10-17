from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'twitter.views.index'),
    url(r'^tweets/', include('twitter.urls', namespace='twitter')),
    url(r'^logout/', 'twitter.views.logout_view', name='logout'),
    url(r'^login/', 'twitter.views.login_view', name='login'),
    url(r'^register/', 'twitter.views.register_view', name='register'),
)