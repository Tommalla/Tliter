from django.http import HttpResponse

from django.core.exceptions import DoesNotExist

from twitter.models import Tweet

def index(request):
	latest_tweets = Tweet.objects.order_by('-pub_date')[:5]
	output = '<br>'.join([t.message for t in latest_tweets])
	return HttpResponse(output)

def show_tweet(request, tweet_id):
	try:
		t = Tweet.objects.get(id=tweet_id)
	except Tweet.DoesNotExist:	#TODO FIXME
		HttpResponse("Tweet %s nonexistent" % tweet_id)
		
	return HttpResponse(t.message)