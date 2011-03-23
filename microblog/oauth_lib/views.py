import cgi, httplib, oauth_zhou
from urllib import urlencode
from urllib import quote as urlquote
from urllib import unquote as urlunquote

# Django
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from backend.models import Member

def douban_login(request):
  mode = request.GET['mode']
  port = request.GET['port']
  turn = request.GET['turn']
  if port == 'douban':
    application_key = "0e614819c5564c9c2b23d84d5002e5d4"
    application_secret = "1024ab5694416153"
  elif port == 'tencent':
    application_key = "61fdb503559f4986888eab11a2e3731c"
    application_secret = "68a7af933a1a1a98ab719df865076ace"
  elif port == 'sina':
    application_key = "499995807"
    application_secret = "5686b57f79ea1ed2cc4398b367a1a1cc"
  elif port == 'netease':
    application_key = "oZJFV7pLBtuE5FUQ"
    application_secret = "K62Zr4qdNEUMItnyMjNiajZtRImt3via"
  else:
    return Http404
  callback_url = "http://%s/oauth/login?mode=verify&port=%s&turn=%s" %(request.get_host,port,turn)
  client = oauth_zhou.get_oauth_client(port,application_key,application_secret,callback_url)
  if mode == "login":
    return HttpResponseRedirect(client.get_authorization_url(request))
  if mode == "verify":
    auth_token = request.GET("oauth_token")
    auth_verifier = request.GET("oauth_verifier")
    port = request.GET('port')
    turn = request.GET('turn')
  user_info = client.get_user_info(auth_token, auth_verifier=auth_verifier)

  return HttpResponseRedirect(turn)

@login_required
def douban_logout(request):
    # Log a user out using Django's logout function and redirect them
    # back to the homepage.
    logout(request)
    return HttpResponseRedirect('/')


def douban_authenticated(request):
  pass

