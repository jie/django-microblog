# encoding: utf-8
from django.forms.models import ModelForm
from django.forms.widgets import TextInput, Textarea
from posts.models import Post


class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ('text', 'slug')
        widgets = {
            'slug': TextInput(attrs={
                'name': 'slug',
                'class': 'span4',
                'placeholder': 'slug',
            }),
            'text': Textarea(attrs={
                'name': 'text',
                'rows': 5,
                'class': 'span4',
                'placeholder': 'content'
            }),
        }
