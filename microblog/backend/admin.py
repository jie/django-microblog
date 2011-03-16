from django import forms
from microblog.backend.models import *
from django.contrib import admin

class TopicAdmin(admin.ModelAdmin):
  list_display = ('id','author','content','conversation','created')
  
class MemberAdmin(admin.ModelAdmin):
  list_display = ('id','nickname','user','protrait')

class MailAdmin(admin.ModelAdmin):
  list_display = ('id','user','recipient','content','created')


admin.site.register(Topic, TopicAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Mail, MailAdmin)