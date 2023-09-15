import hashlib

from django.db import models
from django.utils import timezone

from applications.core.models import Date


class ChannelManager(models.Manager):

    def create_channel(self, name, owner, is_open=True):
        unique_hash = hashlib.sha256(
            name.encode(),
        ).hexdigest()
        channel = self.create(
            name=name,
            unique_hash=unique_hash,
            is_open=is_open,
            owner=owner,
        )
        channel.members.add(owner)
        channel.save()

        return channel


class Channel(Date):

    name = models.CharField(max_length=60)
    unique_hash = models.CharField(
        max_length=255,
        unique=True,
    )
    is_open = models.BooleanField(
        blank=True,
    )
    owner = models.ForeignKey(
        'auth_user.CustomUser',
        on_delete=models.CASCADE,
        related_name='owned_channels',
    )
    members = models.ManyToManyField(
        'auth_user.CustomUser',
        related_name='channels',
        blank=True,
    )

    objects = ChannelManager()

    def __str__(self):
        return self.name


class Message(models.Model):

    content = models.TextField()
    created_at = models.DateTimeField(
        default=timezone.now
    )
    channel = models.ForeignKey(
        'Channel',
        on_delete=models.CASCADE
    )
    owner = models.ForeignKey(
        'auth_user.CustomUser',
        on_delete=models.CASCADE,
        related_name='owned_message',
    )

    class Meta:
        ordering = ['-created_at']
