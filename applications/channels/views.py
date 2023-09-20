import json

from rest_framework import mixins as drf_mixins
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from applications.auth_user.services.hash.hash import get_hash_value
from applications.auth_user.services.users.user import update_user_device
from applications.channels.services.channel.channel import ChannelService
from .models import Channel, Message
from .serializers import ChannelSerializer, MessageSerializer


class MessageViewSet(
    drf_mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """Получить сообщения."""
        user_id = request.user.id
        unique_hash = kwargs.get('unique_hash')
        messages = ChannelService.get_messages(unique_hash, user_id)
        if not messages:
            return Response(
                {'detail': 'Сообщений по данному чату не найдено'},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.serializer_class(messages, many=True)
        return Response(serializer.data)


class ChannelListViewSet(
    drf_mixins.ListModelMixin,
    drf_mixins.CreateModelMixin,
    GenericViewSet,
):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    permission_classes = [IsAuthenticated]


class ChannelDetailViewSet(
    drf_mixins.RetrieveModelMixin,
    drf_mixins.UpdateModelMixin,
    GenericViewSet
):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'unique_hash'

    def partial_update(self, request, *args, **kwargs):
        unique_hash = kwargs.get('unique_hash')
        user = request.user
        channel, message = ChannelService.add_member_to_channel(
            unique_hash=unique_hash,
            user=user
        )
        update_user_device(request)
        if channel:
            return Response(
                {'detail': message},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(
            {'detail': message},
            status=status.HTTP_404_NOT_FOUND
        )


class AddUserToChannelViewSet(
    drf_mixins.UpdateModelMixin,
    GenericViewSet,
):
    permission_classes = [IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        unique_hash = kwargs.get('unique_hash')
        payload = json.loads(get_hash_value(unique_hash))
        email = payload.get('email')
        unique_hash = payload.get('unique_hash')
        if not email or not unique_hash:
            return Response(
                {'detail': 'Не валидный хэш'},
                status=status.HTTP_404_NOT_FOUND,
            )
        channel, message = ChannelService.add_member_to_close_channel(
            user_email=email,
            unique_hash=unique_hash,
        )
        if channel is None:
            return Response(
                {'detail': message},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(
            {'detail': message},
            status=status.HTTP_200_OK,
        )
