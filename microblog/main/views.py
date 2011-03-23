from django.views.generic import list_detail, date_based
from django.contrib.auth.models import User
from backend.models import Topic, Member, FollowRelation
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.db.models import Q

def all_topics(request):
  return list_detail.object_list(
    request,
    queryset = Topic.objects.all().order_by('-created'),
    paginate_by = 10,
    template_name = 'topic/topics_list.html',
    extra_context = {
      'has_side': True,
      'members': Member.objects.all()[:15],
      'page_type':'all',
    },
 )

@login_required
def archieve_topics(request):
  return date_based.archive_index(
    request,
    queryset = Topic.objects.all(),
    date_field = 'created',
    template_name = 'topic/topics_archieve_index.html',
    allow_future = True,
    num_latest = 10,
    allow_empty = True,
  )

@login_required
def me_topics(request):
  my_follower_ship = FollowRelation.objects.filter(user=request.user).filter(follower=request.user)
  try:
    followed = FollowRelation.objects.filter(user=request.user)[:12]
    follower = FollowRelation.objects.filter(follower=request.user)[:12]
  except:
    followed = 0
    follower = 0
  return list_detail.object_list(
    request,
    queryset = Topic.objects.filter(author=request.user).order_by('-created'),
    paginate_by = 10,
    template_name = 'topic/topics_list.html',
    extra_context = {
      'has_side': True,
      'page_type':'me',
      'members': Member.objects.all()[:15],
      'is_followed':my_follower_ship.count(),
      'follower':follower,
      'followed':followed,
    }
  )

@login_required
def people_topics(request, people):
  people = User.objects.get(username=people)
  my_follower_ship = FollowRelation.objects.filter(user=request.user).filter(follower=people)
  try:
    followed = FollowRelation.objects.filter(user=people)[:12]
    follower = FollowRelation.objects.filter(follower=people)[:12]
  except:
    followed = 0
    follower = 0
  return list_detail.object_list(
    request,
    queryset = Topic.objects.filter(author=people).order_by('-created'),
    paginate_by = 10,
    template_name = 'topic/topics_list.html',
    extra_context = {
      'has_side': True,
      'page_type':'people',
      'view_user': people,
      'members': Member.objects.all()[:15],
      'is_followed':my_follower_ship.count(),
      'follower':follower,
      'followed':followed,
    }
  )