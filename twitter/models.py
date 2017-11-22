from django.db import models
from django.utils.text import Truncator
from django.utils.translation import ugettext_lazy as _


class TwitterUser(models.Model):
    owners = models.ManyToManyField(
        'users.User',
        verbose_name=_('Owner')
    )
    twitter_id = models.BigIntegerField(
        _('Twitter Id'),
        unique=True,
        db_index=True
    )
    screen_name = models.CharField(
        _('Twitter username'),
        unique=True,
        max_length=255,
        db_index=True
    )
    name = models.CharField(_('Name'), max_length=255)
    description = models.TextField(_('Description'), blank=True, null=True)

    def __str__(self):
        return self.screen_name

    class Meta:
        verbose_name = _('Twitter User')
        verbose_name_plural = _('Twitter Users')


class Tweet(models.Model):
    twitter_id = models.BigIntegerField(
        _('Twitter Id'),
        unique=True,
        db_index=True
    )
    user = models.ForeignKey(
        'twitter.TwitterUser',
        verbose_name=_('User'),
        db_index=True,
        on_delete=models.CASCADE
    )
    text = models.TextField(_('Content'))
    created_at = models.DateTimeField(_('Posted at'))

    def __str__(self):
        return Truncator(self.text).chars(70)

    class Meta:
        verbose_name = _('Tweet')
        verbose_name_plural = _('Tweets')
        index_together = [['twitter_id', 'user']]
