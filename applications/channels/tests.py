import json
from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory

from applications.auth_user.models import CustomUser
from .models import Channel, Message


class MessageViewSetTest(APITestCase):
    def setUp(self):

        self.user = CustomUser.objects.create_user(email='test@example.ru')
        self.channel = Channel.objects.create_channel("Channel 1", self.user)
        self.unique_hash = self.channel.unique_hash
        self.messages = [
            Message.objects.create(content='lalala', owner=self.user, channel=self.channel),
            Message.objects.create(content='lululu', owner=self.user, channel=self.channel),
        ]

    def test_list_messages_authenticated(self):
        """Тест получения сообщений."""
        self.client.force_authenticate(user=self.user)

        url = reverse('message', kwargs={'unique_hash': self.unique_hash})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(self.messages))


class ChannelListViewSetTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='test@example.ru')

    def test_list_channels_authenticated(self):
        self.client.force_authenticate(user=self.user)

        channels = [
            Channel.objects.create_channel(name='Channel 1', owner=self.user),
            Channel.objects.create_channel(name='Channel 2', owner=self.user),
        ]

        url = reverse('channel')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data['results']), len(channels))

    def test_create_channel_authenticated(self):
        self.client.force_authenticate(user=self.user)

        data = {'name': 'New Channel'}

        url = reverse('channel')

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(Channel.objects.filter(name='New Channel').exists())


class AddUserToChannelViewSetTest(APITestCase):
    def setUp(self):

        self.user = CustomUser.objects.create_user(email='test@example.ru')

        self.channel = Channel.objects.create_channel("Channel 1", self.user)
        self.unique_hash = self.channel.unique_hash

    @patch('applications.channels.views.get_hash_value')
    def test_partial_update_channel(self, mock_get_hash_value):
        self.client.force_authenticate(user=self.user)

        payload = {
            'email': 'test@example.ru',
            'unique_hash': self.unique_hash,
        }
        mock_get_hash_value.return_value = json.dumps(payload)
        url = reverse('add_to_close_channel', kwargs={'unique_hash': self.unique_hash})
        response = self.client.patch(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

