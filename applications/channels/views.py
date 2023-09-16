import json

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins as drf_mixins
from rest_framework import views as drf_view
from rest_framework.viewsets import GenericViewSet
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes

from services.hash.hash import get_hash_value

from .models import Channel
from .serializers import ChannelSerializer, MessageSerializer
from services.channel.channel import ChannelInterface
from services.users.user import update_user_device


class MessageView(drf_view.APIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, unique_hash):
        """Получить сообщения."""
        user_id = request.user.id
        messages = ChannelInterface.get_messages(unique_hash, user_id)
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


class ChannelDetailAPIView(
    generics.RetrieveAPIView,
    generics.UpdateAPIView,
    generics.GenericAPIView,
):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'unique_hash'

    def patch(self, request, *args, **kwargs):
        unique_hash = self.kwargs.get('unique_hash')
        user = request.user
        channel, message = ChannelInterface.add_member_to_channel(
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def add_user_to_channel(request: Request, unique_hash):
    payload = json.loads(get_hash_value(unique_hash))
    email = payload.get('email')
    unique_hash = payload.get('unique_hash')
    if not email or not unique_hash:
        return Response(
            {'detail': 'Не валидный хэш'},
            status=status.HTTP_404_NOT_FOUND,
        )
    channel, message = ChannelInterface.add_member_to_close_channel(
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
