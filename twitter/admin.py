from django.contrib import admin
from twitter.models import Tweet, HashTag

admin.site.register(Tweet)
admin.site.register(HashTag)