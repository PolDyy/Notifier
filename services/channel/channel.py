
from django.core.exceptions import ObjectDoesNotExist

from applications.channels.models import Message, Channel
from services.smtp.smtp import EmailSending
from services.users.user import get_user_by_email


class ChannelInterface:

    @classmethod
    def get_channel(cls, unique_hash):
        try:
            channel = Channel.objects.prefetch_related(
                'members'
            ).select_related(
                'owner'
            ).get(
                unique_hash=unique_hash
            )
        except ObjectDoesNotExist:
            return
        return channel

    @classmethod
    def get_messages(cls, unique_hash):
        channel = cls.get_channel(unique_hash)
        if channel is None:
            return
        messages = Message.objects.select_related(
            'owner',
            'channel'
        ).filter(
            channel=channel
        )

        return messages

    @classmethod
    def get_user_channels(cls, user):
        channels = Channel.objects.prefetch_related(
            'members'
        ).select_related(
            'owner'
        ).filter(members=user)
        return channels

    @classmethod
    def add_member_to_channel(cls, unique_hash, user):
        channel = cls.get_channel(unique_hash)
        if channel is None:
            return None, 'Канал не найден'
        if channel.is_open:
            channel.members.add(user)
            channel.save()
            return channel, 'Вы добавлены в канал'
        EmailSending.send_to_channel_owner(
            channel.owner.email,
            user.email,
            channel.name,
            unique_hash,
        )
        return channel, 'Запрос на добавление в канал отправлен владельцу'

    @classmethod
    def add_member_to_close_channel(cls, unique_hash, user_email):
        channel = cls.get_channel(unique_hash)
        if channel is None:
            return None, 'Канал не найден'
        user = get_user_by_email(user_email)
        channel.members.add(user)
        channel.save()
        return channel, 'Вы добавлены в канал'

