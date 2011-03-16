from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site
from django.template import Context, loader
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.http import int_to_base36
from django.contrib.auth.forms import UserCreationForm
from backend.models import Member
import StringIO

class MyUserSettingsForm(forms.ModelForm):
  class Meta:
    model = Member
    fields = ('nickname', 'protrait')



class MyUserCreationForm(UserCreationForm):
  username = forms.RegexField(label=_("Username"), max_length=30, regex=r'^[\w.@+-]+$',
    help_text = _(u"<span>只含数字字符下划线</span>"),
    error_messages = {'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters.")})
  password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
  password2 = forms.CharField(label=_("Password confirmation"), widget=forms.PasswordInput,
    help_text = _(u"<span>请输入和上面相同的字符</span>"))
  email = forms.CharField(label=_(u"电子邮箱"))
  nickname = forms.CharField(label=_(u"昵称"))
  class Meta:
    model = User
    fields = ("username",)

  def clean_username(self):
    username = self.cleaned_data["username"]
    try:
      User.objects.get(username=username)
    except User.DoesNotExist:
      return username
    raise forms.ValidationError(_("A user with that username already exists."))

  def clean_password2(self):
    password1 = self.cleaned_data.get("password1", "")
    password2 = self.cleaned_data["password2"]
    if password1 != password2:
      raise forms.ValidationError(_("The two password fields didn't match."))
    return password2

  def save(self, commit=True):
    user = super(UserCreationForm, self).save(commit=False)
    user.set_password(self.cleaned_data["password1"])
    user.email = self.cleaned_data["email"]
    nickname = self.cleaned_data["nickname"]
    if commit:
      user.save()
      member = Member(nickname=nickname, user=user)
      member.save()
    return user
