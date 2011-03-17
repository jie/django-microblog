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
    'user':request.user,
    'logined':request.user.is_authenticated(),
    'topics':topics,
    'paginator':paginator,
    'page_type':'index',})

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
    'user':request.user,
    'logined':request.user.is_authenticated(),
    'topics':topics,
    'page_type':'favorite',
    'paginator':paginator,
  })

@login_required
def setfav_view(request):
  if request.method =='POST':
    topic = Topic.objects.get(pk=int(request.POST['id']))
    if request.user in topic.favorites.all():
      topic.favorites.remove(request.user)
      response = HttpResponse('unfav')
    else:
      topic.favorites.add(request.user)
      response = HttpResponse('fav')
    return response

@login_required
def mail_view(request,mailto):
  try:
    recipient = User.objects.get(pk=int(mailto))
  except:
    raise Http404
  if request.method=='POST':
    content = request.POST['content']
    mail = Mail(user=request.user,recipient=recipient,content=content)
    mail.save()
    member = recipient.get_profile()
    try:
      member.unread_count = member.unread_count+1
    except:
      member.unread_count = 0
    member.save()
    return HttpResponseRedirect("/sendbox/")
  else:
    pass
  return render_to_response("mail.html", {
    'recipient':recipient,
    'user':request.user,
    'logined':request.user.is_authenticated(),
    'page_type':'mail',})


@login_required
def inbox_view(request):
  if request.method=='GET':
    mails_all = Mail.objects.all().filter(recipient=request.user).order_by('-created')
    member = request.user.get_profile()
    if member.unread_count !=0:
      member.unread_count = 0
      member.save()
    paginator = Paginator(mails_all, 3)
    try:
      page = int(request.GET.get('page', '1'))
    except ValueError:
      page = 1
    try:
      mails = paginator.page(page)
    except (EmptyPage, InvalidPage):
      mails = paginator.page(paginator.num_pages)
  return render_to_response("inbox.html", {
    'unread_count':request.user.get_profile().unread_count,
    'mails':mails,
    'user':request.user,
    'logined':request.user.is_authenticated(),
    'page_type':'mail',})

@login_required
def sendbox_view(request):
  if request.method=='GET':
    mails_all = Mail.objects.all().filter(user=request.user).order_by('-created')
    paginator = Paginator(mails_all, 3)
    try:
      page = int(request.GET.get('page', '1'))
    except ValueError:
      page = 1
    try:
      mails = paginator.page(page)
    except (EmptyPage, InvalidPage):
      mails = paginator.page(paginator.num_pages)
  return render_to_response("sendbox.html", {
    'mails':mails,
    'user':request.user,
    'logined':request.user.is_authenticated(),
    'page_type':'mail',})



@login_required
def follow_member(request):
  if request.is_ajax():
    try:
      follower = User.objects.get(pk=int(request.raw_post_data))
      my_follower_ship = FollowRelation.objects.filter(user=request.user, follower=follower)
      if len(my_follower_ship):
        my_follower_ship.delete()
      else:
        follow_relation = FollowRelation(user=request.user, follower=follower)
        follow_relation.save()
      response = HttpResponse('success')
      return response
    except:
      pass

@login_required
def delete_topic(request):
  if request.is_ajax():
    try:
      topic = Topic.objects.get(pk=int(request.POST['id']))
      if topic.author == request.user:
          topic.delete()
          return HttpResponse('success')
    except:
      pass

@login_required
def post_topic(request):
  if request.is_ajax():
    try:
      content = smart_unicode(request.raw_post_data)
      topic = Topic(content=content, author=request.user)
      topic.save()
      response = HttpResponse(cgi.escape(topic.content))
      return response
    except:
      pass

@login_required
def post_conversation(request):
  if request.is_ajax():
    try:
      related_topic = Topic.objects.get(pk=int(request.POST['id']))
      topic = Topic(content=request.POST['content'], author=request.user,conversation=related_topic)
      topic.save()
      response = HttpResponse(cgi.escape(topic.content))
      return response
    except:
      pass



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
    'user':request.user,
    'logined':request.user.is_authenticated(),
    'info_form':info_form,
    'password_form':password_form,
  })



@login_required
def logout_view(request):
  auth.logout(request)
  return HttpResponseRedirect("/")

def login_view(request):
  if request.method == 'POST':
    form = AuthenticationForm(data=request.POST)
    if form.is_valid():
      auth.login(request, form.get_user())
      return HttpResponseRedirect("/")
    else:
      return HttpResponseRedirect("/member/login/")
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