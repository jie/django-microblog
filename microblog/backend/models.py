from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from PIL import Image
from urllib2 import unquote
import os
from DictionaryField import DictionaryField


class Member(models.Model):
  user = models.ForeignKey(User,unique=True)
  nickname = models.CharField(_('Nickname'),max_length=6)
  protrait = models.ImageField(_('Protrait'),null=True,blank=True,upload_to='protrait/%Y/%m/%d')
  unread_count = models.IntegerField(null=True,blank=True)
  oauth_data = DictionaryField(null=True,blank=True)
  def gen_unread_count(self):
    if self.unread_count:
      num = self.unread_count
    else:
      num = 0
    return num

  def gen_protrait(self):
    if self.protrait:
      url = self.protrait.url
    else:
      url = '/static/unknow/unkonw_2.png'
    return url

  def gen_username(self):
    return self.user.username

  def save(self, size=(50,50)):
    if self.protrait:

      suffix = os.path.splitext(self.protrait.name)[1]
      self.protrait.save(name='u_'+str(self.user.id)+suffix, content=self.protrait, save=False)

      pw = self.protrait.width
      ph = self.protrait.height
      nw = size[0]
      nh = size[1]
  
      if (pw, ph) != (nw, nh):
        filename = str(self.protrait.path)
        image = Image.open(filename)
        pr = float(pw) / float(ph)
        nr = float(nw) / float(nh)
  
        if pr > nr:
          tw = int(round(nh * pr))
          image = image.resize((tw, nh), Image.ANTIALIAS)
          l = int(round(( tw - nw ) / 2.0))
          image = image.crop((l, 0, l + nw, nh))
        elif pr < nr:
          th = int(round(nw / pr))
          image = image.resize((nw, th), Image.ANTIALIAS)
          t = int(round(( th - nh ) / 2.0))
          print((0, t, nw, t + nh))
          image = image.crop((0, t, nw, t + nh))
        else:
          image = image.resize(size, Image.ANTIALIAS)

        image.save(filename)

    return super(Member, self).save() 


class Topic(models.Model):
  author = models.ForeignKey(User)
  created = models.DateTimeField(auto_now_add=True)
  content = models.TextField()
  conversation = models.ForeignKey('self',null=True,blank=True)
  favorites = models.ManyToManyField(User, related_name='fav')

  def get_fav_users(self):
    return self.favorites.all()


class FollowRelation(models.Model):
  user = models.ForeignKey(User)
  follower = models.ForeignKey(User, related_name='+')

class Mail(models.Model):
  user = models.ForeignKey(User)
  recipient= models.ForeignKey(User, related_name='+')
  content = models.TextField()
  created = models.DateTimeField(auto_now_add=True)
  display = models.ManyToManyField(User, related_name='mail_display')