# encoding: utf-8
from django.forms.models import ModelForm
from django.forms.widgets import TextInput, CheckboxInput, Textarea
# SelectMultiple
from smartcode.models import Post


class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ('text', 'slug', 'is_publish')
        widgets = {
            'slug': TextInput(attrs={
                'name': 'slug',
                'class': 'input-large',
                'placeholder': 'slug',
            }),
            'text': Textarea(attrs={
                'name': 'text',
                'cols': 60,
                'rows': 20,
                'placeholder': 'content'
            }),
            'is_publish': CheckboxInput(attrs={
                'is_publish': 'is_publish',
                'class': 'input-normal',
                'placeholder': 'is_publish'
            }),
        }
