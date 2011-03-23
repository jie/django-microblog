from django.db import models
from django.contrib.auth.models import User

class TencentOauthData(models.Model):
  user = models.ForeignKey(User)
  request_key = models.CharField(verbose_name='Request Key', max_length=30)
  request_secret = models.CharField(verbose_name='Request Secret',max_length=30)
  access_key = models.CharField(verbose_name='Access Key', max_length=30)
  access_secret = models.CharField(verbose_name='Access Secret', max_length=30)