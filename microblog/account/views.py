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
from django.template import RequestContext as RC

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
    'form': form,
  },context_instance=RC(request))


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
  'form': form,
  },context_instance=RC(request))

