from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response,get_object_or_404
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from backend.models import Mail
from django.template import RequestContext as RC
from django.views.generic import list_detail, create_update
from django.contrib import messages
def inbox_generic_view(request):
  return list_detail.object_list(
    request,
    queryset=Mail.objects.filter(user=request.user).order_by('-created'),
    template_name='mail/mail_list.html',
    paginate_by=5,
    )

def sendbox_generic_view(request):
  return list_detail.object_list(
    request,
    queryset=Mail.objects.filter(recipient=request.user).order_by('created'),
    template_name='mail/mail_list.html',
    paginate_by=5,
    )

def delete_mail_generic_view(request, object_id):
  return create_update.delete_object(
    request,
    model=Mail,
    object_id = int(object_id),
    post_delete_redirect='/mail/generic/inbox/',
    template_name='mail/mail_confirm_delete.html',
    extra_context={'mail':get_object_or_404(Mail, pk=int(object_id)),}
  )

@login_required
def delete_mail(request, mail_id):
  if request.method=='GET':
    mail = get_object_or_404(Mail, pk=int(mail_id))
    redirect_to = request.GET.get('go')
    if mail.user == request.user:
      mail.delete()
      return HttpResponseRedirect(redirect_to)

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
    messages.add_message(request, messages.SUCCESS, 'Mail send successfully')
    member = recipient.get_profile()
    try:
      member.unread_count = member.unread_count+1
    except:
      member.unread_count = 0
    member.save()
    return HttpResponseRedirect("/mail/sendbox/")
  else:
    pass
  return render_to_response("mail.html", {
    'recipient':recipient,
    'page_type':'mail',
    },context_instance=RC(request))


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
    'page_type':'mail',
    'paginator':paginator,
    },context_instance=RC(request))

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
    'page_type':'mail',
    'paginator':paginator,
    },context_instance=RC(request))

