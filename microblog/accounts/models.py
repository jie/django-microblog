from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User


class Profiles(models.Model):
    user = models.OneToOneField(User)
    oauth_id = models.CharField(max_length=200)
    screen_name = models.CharField(max_length=50)
    access_token = models.CharField(max_length=200)
    avatar = models.URLField(max_length=200)
    location = models.CharField(max_length=200)
    province = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    last_ip = models.IPAddressField()
    current_status = models.CharField(max_length=300)
    description = models.TextField()

    class Meta:
        db_table = u'mp_profile'


admin.site.register(Profiles)
