from django.db import models
from django.utils.translation import ugettext_lazy as _


class TwitterUser(models.Model):
    twitter_id = models.BigIntegerField(_('Twitter Id'), unique=True)
    screen_name = models.CharField(_('Twitter username'),
                                   unique=True, max_length=255)
    name = models.CharField(_('Name'), max_length=255)


class Tweet(models.Model):
    user = models.ForeignKey(
        'twitter.TwitterUser',
        verbose_name=_('User'),
        on_delete=models.CASCADE
    )
    content = models.TextField(_('Content'))
    posted_at = models.DateTimeField(_('Posted at'))
