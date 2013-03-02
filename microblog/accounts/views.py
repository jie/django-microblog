# encoding: utf-8
from pyoauth2 import Client
from accounts.oauth2_configs import *
from accounts.models import Profiles
from django.shortcuts import redirect
from django.template.response import TemplateResponse as render
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

client = Client(client_id=weibo_key,
                client_secret=weibo_secret,
                site=weibo_site_url,
                authorize_url=weibo_authorize_url,
                token_url=weibo_access_token_url
                )


def login_view(request):
    next = request.GET.get("next")
    if request.user.is_authenticated():
        return redirect(next or "settings_view")
    authorize_url = client.auth_code.authorize_url(
        redirect_uri=weibo_callback_url)
    return HttpResponseRedirect(authorize_url)


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')


def authorize_view(request):
    code = request.GET.get('code', None)
    if not code:
        msg = 'login callback error'
        messages.error(request, msg)
        raise Exception(msg)
    code = code.strip()
    access_token = client.auth_code.get_token(code,
                                              redirect_uri=weibo_callback_url,
                                              header_format='OAuth2 %s'
                                              )
    weibo_uid = access_token.params.get('uid')
    oauth_id = "%s@weibo" % str(weibo_uid)
    ret = access_token.get(weibo_user_info_url, uid=weibo_uid)
    userinfo = ret.parsed

    try:
        user = User.objects.get(username__exact=oauth_id)
        profile = user.get_profile()
    except User.DoesNotExist:
        user = User.objects.create_user(oauth_id)
        user.set_password(oauth_id)
        user.save()
        profile = Profiles()
        profile.user = user
        profile.oauth_id = oauth_id

    profile.screen_name = userinfo.get('screen_name').encode('utf-8')
    profile.access_token = access_token.token
    profile.avatar = userinfo.get('profile_image_url')
    profile.location = userinfo.get(
        'location').strip().encode('unicode_escape')
    profile.province = userinfo.get('province')
    profile.city = userinfo.get('city')
    profile.last_ip = request.META.get('REMOTE_ADDR')
    profile.current_status = userinfo.get(
        'status').get('text').strip().encode('unicode_escape')
    profile.description = userinfo.get('description').strip().encode('utf-8')
    profile.save()
    accounts = authenticate(username=oauth_id, password=oauth_id)
    login(request, accounts)
    request.session['profile'] = profile
    return redirect('settings_view')


@login_required
def settings_view(request):
    params = dict(current_page='settings_view')
    return render(request, 'accounts/settings.html', params)
