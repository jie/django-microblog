# encoding: utf-8
import qrcode
from django.http import HttpResponse
from django.template.response import TemplateResponse as render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from smartcode.models import Post
from smartcode.forms import PostForm


def home(request):
    params = dict(current_page='home')
    return render(request, 'smartcode/home.html', params)


@login_required
def create_post_view(request):
    params = dict(current_page='create_post')
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            slug = form.cleaned_data['slug']
            text = form.cleaned_data['text']
            post = Post(slug=slug, text=text)
            try:
                post.user = request.user
                post.save()
                redirect('post_detail_view')
            except Exception, e:
                messages.error(request, "create post errors: %s" % e)
        else:
            messages.error(request, "form errors: %s" % form.errors)
    else:
        form = PostForm()
    params.update(form=form)
    return render(request, 'smartcode/create_post.html', params)


@login_required
def posts_list_view(request):
    params = dict()
    posts = Post.objects.filter(user=request.user, is_enabled=True)
    params.update(posts=posts)
    return render(request, 'smartcode/posts_list.html', params)


@login_required
def post_detail_view(request, post_slug):
    params = dict()
    try:
        post = Post.objects.get(slug=post_slug)
    except:
        messages.warn(request, 'post with slug: %s not found' % post_slug)
        post = None

    params.update(post=post)
    return render(request, 'smartcode/post_detail.html', params)


@login_required
def create_smartcode_view(request, post_id):
    post = Post.objects.get(pk=post_id)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )
    qr.add_data(post.text)
    qr.make(fit=True)
    img = qr.make_image()
    response = HttpResponse(img, content_type='image/png')
    response['Content-Disposition'] = 'attachment; filename="foo.xls"'
    return response
