from django.db import models
from django.contrib.auth.models import User

class Tweet(models.Model):
	message = models.TextField(blank=False)
	pub_date = models.DateTimeField('date published',blank=False)
	hashtags = models.ManyToManyField('HashTag')
	author = models.ForeignKey(User)
	
	def __unicode__(self):
		return self.message
	
class HashTag(models.Model):
	name = models.CharField(max_length=200,blank=False,unique=True)
	
	def __unicode__(self):
		return 'haszTag' + self.name
