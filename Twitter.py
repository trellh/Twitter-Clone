INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'stream_twitter',
    'stream_django'
)

from django.db import models, connection
from django.conf import settings as django_settings
from datetime import datetime, timedelta
from email.utils import parsedate
from django.utils import timezone
import os
import socket
from . import settings
from django.core.exceptions import ObjectDoesNotExist
from swapper import swappable_setting
from . import fields

class Tweet(models.Model):
    user = models.ForeignKey('auth.User')
    text = models.CharField(max_length=160)
    created_at = models.DateTimeField(auto_now_add=True)


class Follow(models.Model):
    user = models.ForeignKey('auth.User', related_name='friends')
    target = models.ForeignKey('auth.User', related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'target')

from django.views.generic.edit import CreateView
from stream_twitter.models import Follow
from stream_twitter.models import Tweet


class TweetView(CreateView):
    model = Tweet
    fields = ['text']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(Tweet, self).form_valid(form)
