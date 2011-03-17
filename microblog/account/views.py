import time
import random
import cgi
import settings
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,PasswordChangeForm
from backend.forms import MyUserSettingsForm, MyUserCreationForm
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from backend.models import Member, Topic, FollowRelation, Mail
from django.utils.encoding import smart_unicode
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import Q
from django.contrib.auth import REDIRECT_FIELD_NAME


@login_required
def logout_view(request):
  auth.logout(request)
  return HttpResponseRedirect("/")

def login_view(request,redirect_field_name=REDIRECT_FIELD_NAME):
  redirect_to = request.REQUEST.get(redirect_field_name, '')
  if request.method == 'POST':
    form = AuthenticationForm(data=request.POST)

    if form.is_valid():
      if not redirect_to or ' ' in redirect_to:
        redirect_to = settings.LOGIN_REDIRECT_URL
      elif '//' in redirect_to and re.match(r'[^\?]*//', redirect_to):
        redirect_to = settings.LOGIN_REDIRECT_URL
      auth.login(request, form.get_user())

      if request.session.test_cookie_worked():
        request.session.delete_test_cookie()

      return HttpResponseRedirect(redirect_to)

  else:
    form = AuthenticationForm()
  return render_to_response("login.html", {
  'form': form,'user':request.user,'logined':request.user.is_authenticated()
  })


def signup_view(request):
  if request.method == 'POST':
    form = MyUserCreationForm(request.POST)
    if form.is_valid():
      new_user = form.save()
      new_user.backend="%s.%s" %('django.contrib.auth.backends','ModelBackend')
      auth.login(request, new_user)
      return HttpResponseRedirect("/")
  else:
    form = MyUserCreationForm()
  return render_to_response("signup.html", {
  'form': form,'user':request.user,'logined':request.user.is_authenticated()
  })

@login_required
def self_view(request):
  if request.method == 'GET':
    try:
      followed = FollowRelation.objects.filter(user=request.user)[:12]
      follower = FollowRelation.objects.filter(follower=request.user)[:12]
    except:
      followed = 0
      follower = 0
    topics_all = Topic.objects.filter(Q(author=request.user)|Q(conversation__author=request.user)).order_by('-created')
    topics_count = topics_all.count()
    members = Member.objects.all()
    paginator = Paginator(topics_all, 10)
    try:
      page = int(request.GET.get('page', '1'))
    except ValueError:
      page = 1
    try:
      topics = paginator.page(page)
    except (EmptyPage, InvalidPage):
      topics = paginator.page(paginator.num_pages)

  return render_to_response("self.html", {
    'user':request.user,
    'logined':request.user.is_authenticated(),
    'topics':topics,
    'members':members,
    'paginator':paginator,
    'follower':follower,
    'followed':followed,
    'page_type': 'self',
  })


@login_required
def member_view(request, user_name):
  if request.method == 'GET':
    view_user = User.objects.get(username=user_name)
    my_follower_ship = FollowRelation.objects.filter(user=request.user).filter(follower=view_user)
    topics_all = Topic.objects.filter(author=view_user).order_by('-created')
    topics_count = topics_all.count()
    paginator = Paginator(topics_all, 10)
    members = Member.objects.all()
    try:
      followed = FollowRelation.objects.filter(user=view_user)[:12]
      follower = FollowRelation.objects.filter(follower=view_user)[:12]
    except:
      followed = 0
      follower = 0
    try:
      page = int(request.GET.get('page', '1'))
    except ValueError:
      page = 1
    try:
      topics = paginator.page(page)
    except (EmptyPage, InvalidPage):
      topics = paginator.page(paginator.num_pages)
  return render_to_response("member.html", {
    'user':request.user,
    'logined':request.user.is_authenticated(),
    'topics':topics,
    'members':members,
    'topics_count':topics_count,
    'view_user':view_user,
    'nickname':view_user.get_profile().nickname,
    'is_followed':len(my_follower_ship),
    'page_type':'member',
    'follower':follower,
    'followed':followed,
  })