# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.contrib.auth import authenticate, logout, login
from django.core.urlresolvers import reverse
from django.contrib import messages

from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from twitter.models import Tweet

def getTweetsPage(request, tweets):
    paginator = Paginator(tweets, 7) # Show per page

    page = request.GET.get('page')
    try:
        res = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        res = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        res = paginator.page(paginator.num_pages)

    return res

def display_tweets(request, tweets, can_add):
	context = {'tweets': tweets, 'can_tweet' : can_add and request.user.is_authenticated()}
	return render(request, 'twitter/show_tweets.html', context)

def index(request):
	latest_tweets = getTweetsPage(request, Tweet.objects.order_by('-pub_date'))
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
		tweets = getTweetsPage(request, Tweet.objects.filter(author=u).order_by('-pub_date'))
		out = display_tweets(request, tweets, False)
	except Tweet.DoesNotExist:
		out = HttpResponse("Wrong input")
	return out

def add(request):
	t = Tweet(message=request.POST['message'], pub_date=timezone.now(), author=request.user)
	t.save()
	return HttpResponseRedirect(reverse('twitter:index'))

def login_view(request):
	username = request.POST['username'] if 'username' in request.POST else '';
	password = request.POST['password'] if 'password' in request.POST else '';

	if not password or not username:
		messages.add_message(request, messages.ERROR, 'Błąd! Musisz wypełnić wszystkie pola!' )
	else:
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
		else:
			messages.add_message(request, messages.ERROR, 'Użyszkodnik nie istnieje!')
	
	return HttpResponseRedirect(reverse('twitter:index'))

def logout_view(request):
	logout(request)
	messages.add_message(request, messages.INFO, 'Wylogowano.')
	return HttpResponseRedirect(reverse('twitter:index'))

def show_registration(request, usernameCallback=None):
	return render(request, 'twitter/register.html', {'can_register' : not request.user.is_authenticated(), 'username' : usernameCallback})

def register_view(request):
	if 'post' in request.POST:
		#TODO IN!
		username = request.POST['username'] if 'username' in request.POST else '';
		password = request.POST['password'] if 'password' in request.POST else '';
	
		error = False
	
		if username and User.objects.filter(username=username).count():
			error = True
			messages.add_message(request, messages.ERROR, 'Błąd! Użyszkodnik o takiej nazwie już istnieje!')
			
		if not password or not username:
			error = True
			messages.add_message(request, messages.ERROR, 'Błąd! Musisz wypełnić wszystkie pola!' )
		
		if error:
			return show_registration(request, username)
		
		User.objects.create_user(username=username, password=password)
		messages.add_message(request, messages.INFO, 'Pomyślnie utworzono użyszkodnika.')
		return login_view(request)
	else:
		return render(request, 'twitter/register.html',  {'can_register' : not request.user.is_authenticated()})