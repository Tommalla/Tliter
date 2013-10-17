from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.contrib.auth import authenticate, logout, login

from django.contrib.auth.models import User
from twitter.models import Tweet

def display_tweets(request, tweets, can_add):
	context = {'tweets': tweets, 'can_tweet' : can_add and request.user.is_authenticated()}
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

def tweets_by(request, username):
	out = None
	try:
		u = get_object_or_404(User, username=username)
		tweets = Tweet.objects.filter(author=u).order_by('-pub_date')
		out = display_tweets(request, tweets, False)
	except Tweet.DoesNotExist:
		out = HttpResponse("Wrong input")
	return out

def add(request):
	t = Tweet(message=request.POST['message'], pub_date=timezone.now(), author=request.user)
	t.save()
	return HttpResponseRedirect('/tweets')

def login_view(request):
	username = request.POST['login']
	password = request.POST['password']
	user = authenticate(username=username, password=password)
	if user is not None:
		if user.is_active:
			login(request, user)
	else:
		return HttpResponse("User nonexistent");
	return HttpResponseRedirect('/')

def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')

def register_view(request):
	#TODO
	return HttpResponse('TODO');