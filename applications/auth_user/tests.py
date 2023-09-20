from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import CustomUser
from .services.token import token


class SendAuthEmailViewTests(APITestCase):
    def test_send_auth_email_success(self):
        "Валидные тест отправки сообщения."
        url = reverse('auth-email')
        data = {'email': 'test@example.com'}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                'success': True,
                'message': 'Ссылка для входа отправлена на почту'
            }
        )

    def test_send_auth_email_invalid_data(self):
        """Тест отправки сообщения на почту с невалидным полем."""
        url = reverse('auth-email')
        data = {'email': 'invalid_email'}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {
                'success': False,
                'message': 'Проверьте правильность заполнения формы.'
            }
        )


class LoginUserViewTests(APITestCase):
    def test_login_user_view(self):
        """Тест аутентификации пользователя."""
        with patch(
                'applications.auth_user.views.get_hash_value',
                return_value='test@example.com'
        ):
            url = reverse('login', args=['your_unique_hash'])
            response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data.get('access_token'))
        self.assertTrue('refresh_token' in response.cookies)


class RefreshTokenViewTests(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(email='test@example.ru')
        self.access_token = token.generate_access_token(self.user.email)
        self.refresh_token = token.generate_refresh_token(self.user.email)

    def test_refresh_token_view(self):
        """Тест обновления токена."""
        headers = {
            'Authorization': f'Token {self.access_token}',
        }

        self.client.cookies['refresh_token'] = self.refresh_token
        url = reverse('refresh')
        response = self.client.post(url, headers=headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access_token' in response.data)

    def test_refresh_token_view_invalid(self):
        """Тест обновления токена без refresh токена."""
        headers = {
            'Authorization': f'Token {self.access_token}',
        }

        url = reverse('refresh')
        response = self.client.post(url, headers=headers)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

