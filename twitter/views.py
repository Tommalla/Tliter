from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from twitter.models import Tweet

def display_tweets(request, tweets, can_add):
	context = {'tweets': tweets, 'logged' : can_add}
	return render(request, 'twitter/show_tweets.html', context)

def index(request):
	latest_tweets = Tweet.objects.order_by('-pub_date')[:5]	
	return display_tweets(request, latest_tweets, True) #FIXME: can_add depending on login 

def show_tweet(request, tweet_id):
	out = None
	try:
		t = get_object_or_404(Tweet, id=tweet_id)
		out = display_tweets(request, {t}, False)
	except Tweet.DoesNotExist:
		out = HttpResponse("Tweet %s nonexistent" % tweet_id)
		
	return out

def add(request):
	t = Tweet(message=request.POST['message'], pub_date=timezone.now())
	t.save()
	return HttpResponseRedirect('/tweets')

def login(request):
	#TODO
	return HttpResponseRedirect('/')

def logout(request):
	#TODO
	return HttpResponseRedirect('/')