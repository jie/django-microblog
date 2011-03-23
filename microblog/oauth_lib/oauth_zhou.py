from cgi import parse_qs
from django.utils import simplejson as json
from hashlib import sha1
from hmac import new as hmac
from random import getrandbits
from time import time
from urllib import urlencode
from urllib import quote as urlquote
from urllib import unquote as urlunquote
import urllib2
import logging

class OAuthException(Exception):
    pass

def get_oauth_client(service, key, secret, callback_url):
  """Get OAuth Client.

  A factory that will return the appropriate OAuth client.
  """

  if service == "twitter":
    return TwitterClient(key, secret, callback_url)
  elif service == "yahoo":
    return YahooClient(key, secret, callback_url)
  elif service == "douban":
    return DoubanClient(key, secret, callback_url)
  elif service == "tencent":
    return TencentClient(key, secret, callback_url)
  elif service == "sina":
    return SinaClient(key, secret, callback_url)
  elif service == "netease":
    return NeteaseClient(key, secret, callback_url)
  else:
    raise Exception, "Unknown OAuth service %s" % service

class OAuthClient():
  def __init__(self, service_name, consumer_key, consumer_secret, request_url, access_url, callback_url=None):
    """ Constructor."""
    self.service_name = service_name
    self.consumer_key = consumer_key
    self.consumer_secret = consumer_secret
    self.request_url = request_url
    self.access_url = access_url
    self.callback_url = callback_url

  def prepare_request(self, url, token="", secret="", additional_params=None, method='GET'):
    """Prepare Request.
    Prepares an authenticated request to any OAuth protected resource.
    Returns the payload of the request.
    """

    def encode(text):
      return urlquote(str(text), "")

    params = {
      "oauth_consumer_key": self.consumer_key,
      "oauth_signature_method": "HMAC-SHA1",
      "oauth_timestamp": str(int(time())),
      "oauth_nonce": str(getrandbits(64)),
      "oauth_version": "1.0"
    }

    if token:
      params["oauth_token"] = token
    elif self.callback_url:
      params["oauth_callback"] = self.callback_url

    if additional_params:
        params.update(additional_params)

    for k,v in params.items():
        if isinstance(v, unicode):
            params[k] = v.encode('utf8')

    # Join all of the params together.
    params_str = "&".join(["%s=%s" % (encode(k), encode(params[k])) for k in sorted(params)])

    # Join the entire message together per the OAuth specification.
    message = "&".join(["GET" if method == "GET" else "POST", encode(url), encode(params_str)])

    # Create a HMAC-SHA1 signature of the message.
    key = "%s&%s" % (self.consumer_secret, secret) # Note compulsory "&".
    signature = hmac(key, message, sha1)
    digest_base64 = signature.digest().encode("base64").strip()
    params["oauth_signature"] = digest_base64

    # Construct the request payload and return it
    return urlencode(params)

  def make_async_request(self, url, token="", secret="", additional_params=None,
                   protected=False, method="GET"):
    """Make Request.
    Make an authenticated request to any OAuth protected resource.
    If protected is equal to True, the Authorization: OAuth header will be set.
    A urlfetch response object is returned."""

    payload = self.prepare_request(url, token, secret, additional_params, method)
    if method == 'GET':
        url = "%s?%s" % (url, payload)
        payload = None
    fetcher = urllib2.Request(url)
    if protected:
      fetcher.add_header("Authorization", "OAuth")
    response = urllib2.urlopen(url=fetcher, data=payload)
    return response

  def make_request(self, url, token="", secret="", additional_params=None, protected=False, method='GET'):
    return self.make_async_request(url, token, secret, additional_params, protected, method).read()

  def get_authorization_url(self):
    """
    Get Authorization URL.
    Returns a service specific URL which contains an auth token. The user
    should be redirected to this URL so that they can give consent to be
    logged in.
    """

    raise NotImplementedError, "Must be implemented by a subclass"

  def get_user_info(self, request, auth_token, auth_verifier=""):
    """
    Get User Info.
    Exchanges the auth token for an access token and returns a dictionary
    of information about the authenticated user.
    """

    auth_token = urlunquote(auth_token)
    auth_verifier = urlunquote(auth_verifier)

    auth_secret = request.session['request_token']['oauth_token_secret']

    response = self.make_request(self.access_url,
                                token=auth_token,
                                secret=auth_secret,
                                additional_params={"oauth_verifier":auth_verifier})

    # Extract the access token/secret from the response.
    result = self._extract_credentials(response)

    # Try to collect some information about this user from the service.
    user_info = self._lookup_user_info(result["token"], result["secret"])
    return user_info

  def _get_auth_token(self, request):
    """Get Authorization Token.
    Actually gets the authorization token and secret from the service. The
    token and secret are stored in our database, and the auth token is
    returned.
    """
    response = self.make_request(self.request_url)
    result = self._extract_credentials(response)

    auth_token = result["token"]
    auth_secret = result["secret"]

    request.session['request_token'] = result

    return auth_token


  def _extract_credentials(self, result):
    """Extract Credentials.

    Returns an dictionary containing the token and secret (if present).
    Throws an Exception otherwise.
    """

    token = None
    secret = None
    raise('data is %s' %result)
    parsed_results = parse_qs(result.content)

    if "oauth_token" in parsed_results:
      token = parsed_results["oauth_token"][0]

    if "oauth_token_secret" in parsed_results:
      secret = parsed_results["oauth_token_secret"][0]

    if not (token and secret) or result.status_code != 200:
      logging.error("Could not extract token/secret: %s" % result.content)
      raise OAuthException("Problem talking to the service")

    return {
      "service": self.service_name,
      "token": token,
      "secret": secret
    }

  def _lookup_user_info(self, access_token, access_secret):
    """Lookup User Info.

    Complies a dictionary describing the user. The user should be
    authenticated at this point. Each different client should override
    this method.
    """

    raise NotImplementedError, "Must be implemented by a subclass"

  def _get_default_user_info(self):
    """Get Default User Info.

    Returns a blank array that can be used to populate generalized user
    information.
    """

    return {
      "id": "",
      "username": "",
      "name": "",
      "picture": ""
    }

  def oauth_user_info(self):
    """Get Default User Info.

    Returns a blank array that can be used to populate generalized user
    information.
    """

    return {
      "name": "",
      "signature": "",
      "link": "",
      "portrait": "",
      "port": "",
      "sex": ""
    }

class DoubanClient(OAuthClient):
  def __init__(self, consumer_key, consumer_secret, callback_url):
    OAuthClient.__init__(self,
        "douban",
        consumer_key,
        consumer_secret,
        "http://www.douban.com/service/auth/request_token",
        "http://www.douban.com/service/auth/access_token",
        callback_url)

  def get_authorization_url(self,request):
    token = self._get_auth_token(request)
    return ("http://www.douban.com/service/auth/authorize?oauth_token=%s" "&oauth_callback=%s" % (token, urlquote(self.callback_url)))

  def _lookup_user_info(self, access_token, access_secret):
    response = self.make_request("http://api.douban.com/people/%40me", token=access_token, secret=access_secret, additional_params={"alt": "json"}, protected=True)
    data = json.loads(response.content)
    user_info = self.oauth_user_info()
    user_info["name"] = data["title"]["$t"].encode('utf-8')
    user_info["signature"] = data["db:signature"]["$t"].encode('utf-8')
    user_info["link"] = data["link"][1]["@href"]
    user_info["portrait"] = data["link"][2]["@href"].replace('\\','')
    user_info["port"] = 'douban'
    user_info["sex"] = 'u'
    return user_info