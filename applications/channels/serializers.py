from django.urls import reverse

from rest_framework import serializers
from .models import Message, Channel


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = (
            'id',
            'channel',
            'content',
            'created_at',
            'owner',
        )
        extra_kwargs ={
            'id': {'read_only': True},
            'created_at': {'read_only': True},
            'owner': {'read_only': True},
        }


class ChannelSerializer(serializers.ModelSerializer):

    url = serializers.SerializerMethodField()

    class Meta:
        model = Channel
        fields = (
            'id',
            'name',
            'owner',
            'unique_hash',
            'created',
            'is_open',
            'url',
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'created': {'read_only': True},
            'owner': {'read_only': True},
            'unique_hash': {'read_only': True},
            'url': {'read_only': True},
        }

    def get_url(self, obj):
        request = self.context.get('request')
        unique_hash_value = obj.unique_hash
        kwargs = {
            'unique_hash': unique_hash_value
        }
        path = reverse('channel-detail', kwargs=kwargs)
        return request.build_absolute_uri(path)

    def create(self, validated_data):
        user = self.context['request'].user
        channel = Channel.objects.create_channel(
            name=validated_data.get('name'),
            owner=user,
            is_open=validated_data.get('is_open')
        )
        return channel

class HashSerializer(serializers.Serializer):
    unique_hash = serializers.CharField(
        max_length=32
    )
