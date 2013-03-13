import base64
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

    class Meta:
        db_table = u'mp_post'


class QRCodeImage(models.Model):
    post = models.ForeignKey(Post, db_column='post')
    width = models.IntegerField()
    height = models.IntegerField()
    mode = models.CharField(max_length=10)
    _data = models.TextField(db_column='data')

    def set_data(self, data):
        self._data = base64.encodestring(data)

    def get_data(self):
        return base64.decodestring(self._data)

    data = property(get_data, set_data)

    class Meta:
        db_table = u'mp_qrcode'
