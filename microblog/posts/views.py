# encoding: utf-8
import Image
import qrcode
import StringIO
from django.http import HttpResponse
from django.template.response import TemplateResponse as render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from posts.models import Post, QRCodeImage
from posts.forms import PostForm


def home(request):
    params = dict(current_page='home')
    return render(request, 'posts/home.html', params)


@login_required
def create_post_view(request):
    params = dict(current_page='create_post')
    if request.method == 'POST':
        form = PostForm(request.POST, auto_id=False)
        if form.is_valid():
            slug = form.cleaned_data['slug']
            text = form.cleaned_data['text']
            post = Post(slug=slug, text=text)
            try:
                post.user = request.user
                post.save()
                return redirect('post_detail_view', post.slug)
            except Exception, e:
                messages.error(request, "create post errors: %s" % e)
        else:
            messages.error(request, "form errors: %s" % form.errors)
    else:
        form = PostForm(auto_id=False)
    params.update(form=form)
    return render(request, 'posts/create_post.html', params)


@login_required
def posts_list_view(request):
    params = dict()
    posts = Post.objects.filter(user=request.user, is_enabled=True)
    params.update(posts=posts)
    return render(request, 'posts/posts_list.html', params)


@login_required
def post_detail_view(request, post_slug):
    params = dict()
    try:
        post = Post.objects.get(slug=post_slug)
    except:
        messages.warning(request, 'post with slug: %s not found' % post_slug)
        post = None

    params.update(post=post)
    return render(request, 'posts/post_detail.html', params)


@login_required
def create_qrcode_view(request, post_id):
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
    qrImage = QRCodeImage()
    io = StringIO.StringIO()
    img.save(io, 'PNG')
    qrImage.data = io.getvalue()
    io.close()
    qrImage.post = post
    qrImage.mode = img._img.mode
    qrImage.width, qrImage.height = img._img.size
    qrImage.save()
    return redirect('qrcode_image_view', '%s' % post.slug)


def qrcode_image_view(request, post_slug):
    qrImage = QRCodeImage.objects.get(post__slug=post_slug)
    io = StringIO.StringIO(qrImage.data)
    response = HttpResponse(io, content_type='image/png')
    #response['Content-Disposition'] = 'attachment; filename="%s.png"' % post_slug
    response['Content-Disposition'] = 'inline; filename="%s.png"' % post_slug
    return response
