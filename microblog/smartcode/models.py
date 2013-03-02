from django.db import models
from django.contrib.auth.models import User


RATING_CHOICES = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
)


class Post(models.Model):
    user = models.ForeignKey(User)
    text = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)
    is_enabled = models.BooleanField(default=True)
    is_publish = models.BooleanField(default=True)
    rating = models.CharField(blank=True,
                              max_length=2,
                              choices=RATING_CHOICES
                              )
