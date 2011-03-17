# # -*- coding: utf-8 -*-  
import time
import random
import cgi
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,PasswordChangeForm
from backend.forms import MyUserSettingsForm, MyUserCreationForm
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response
from django.utils import simplejson
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from backend.models import Member, Topic, FollowRelation, Mail
from django.utils.encoding import smart_unicode
from urllib2 import unquote
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import Q
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.template import RequestContext as RC

@login_required
def index(request):
  members = Member.objects.all()
  topics_all = Topic.objects.all().order_by('-created')
  paginator = Paginator(topics_all, 10)
  try:
    page = int(request.GET.get('page', '1'))
  except ValueError:
    page = 1
  try:
    topics = paginator.page(page)
  except (EmptyPage, InvalidPage):
    topics = paginator.page(paginator.num_pages)
  return render_to_response("index.html", {
    'members':members,
    'topics':topics,
    'paginator':paginator,
    'page_type':'index',
    },context_instance=RC(request))

@login_required
def favorite_view(request):
  topics_all = request.user.fav.all().order_by('-created')
  paginator = Paginator(topics_all, 10)
  try:
    page = int(request.GET.get('page', '1'))
  except ValueError:
    page = 1
  try:
    topics = paginator.page(page)
  except (EmptyPage, InvalidPage):
    topics = paginator.page(paginator.num_pages)

  return render_to_response("favorite.html",{
    'topics':topics,
    'page_type':'favorite',
    'paginator':paginator,
  },context_instance=RC(request))

@login_required
def setfav_view(request):
  assert(request.method =='POST' and request.is_ajax() == True)
  topic = Topic.objects.get(pk=int(request.POST['id']))
  if request.user in topic.favorites.all():
    topic.favorites.remove(request.user)
    response = HttpResponse('unfav')
  else:
    topic.favorites.add(request.user)
    response = HttpResponse('fav')
  return response


@login_required
def follow_member(request):
  assert(request.method=='POST' and request.is_ajax()==True)
  try:
    follower = User.objects.get(pk=int(request.raw_post_data))
    my_follower_ship = FollowRelation.objects.filter(user=request.user, follower=follower)
    if len(my_follower_ship):
      my_follower_ship.delete()
    else:
      follow_relation = FollowRelation(user=request.user, follower=follower)
      follow_relation.save()
    return HttpResponse('success')
  except:
    return HttpResponse('fail')

@login_required
def delete_topic(request):
  assert(request.method=='POST' and request.is_ajax()==True)
  topic = Topic.objects.get(pk=int(request.POST['id']))
  if topic.author == request.user:
    topic.delete()
    return HttpResponse('success')
  else:
    return HttpResponse('fail')

@login_required
def post_topic(request):
  assert(request.method=='POST' and request.is_ajax()==True)
  content = smart_unicode(request.raw_post_data)
  topic = Topic(content=content, author=request.user)
  topic.save()
  response = HttpResponse(cgi.escape(topic.content))
  return response

@login_required
def post_conversation(request):
  assert(request.method=='POST' and request.is_ajax()==True)
  related_topic = Topic.objects.get(pk=int(request.POST['id']))
  topic = Topic(content=request.POST['content'], author=request.user,conversation=related_topic)
  topic.save()
  response = HttpResponse(cgi.escape(topic.content))
  return response


@login_required
def settings_view(request):
  try:
    info = Member.objects.get(user=request.user)
  except:
    info = Member(user=request.user)
  if request.method == 'POST':
    info_form = MyUserSettingsForm(request.POST, request.FILES, instance=info)
    password_form = PasswordChangeForm(request.user,request.POST)
    if info_form.is_valid():
      info_form = info_form.save()
    if password_form .is_valid():
      password_form.clean_old_password()
      password_form  = password_form.save()
    return HttpResponseRedirect("/settings/")
  else:
    info_form = MyUserSettingsForm(instance=info)
    password_form = PasswordChangeForm(request.user,request.GET)
  return render_to_response("settings.html", {
    'info_form':info_form,
    'password_form':password_form,
  },context_instance=RC(request))
