from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import exceptions
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from applications.auth_user.serializers import AuthSerializer
from applications.auth_user.services.hash.hash import get_hash_value
from applications.auth_user.services.smtp.smtp import EmailSending
from applications.auth_user.services.token import token
from applications.auth_user.services.users import user


class SendAuthEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request):
        """Отправка на почту сообщения для входа."""
        serializer = AuthSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            EmailSending.send_auth_email(email)
            return Response(
                {
                    'success': True,
                    'message': 'Ссылка для входа отправлена на почту'
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                'success': False,
                'message': 'Проверьте правильность заполнения формы.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )


class LoginUserView(APIView):
    permission_classes = [AllowAny]

    @method_decorator(ensure_csrf_cookie)
    def get(self, request: Request, unique_hash: str):
        email = get_hash_value(unique_hash)
        if not email or not isinstance(email, str):
            raise exceptions.AuthenticationFailed(
                'Невалидная ссылка авторизации',
            )
        user.create_user_if_not_exists(email)
        access_token = token.generate_access_token(email)
        refresh_token = token.generate_refresh_token(email)
        response = Response()
        response.set_cookie(key='refresh_token', value=refresh_token, httponly=True)
        response.data = {
            'access_token': access_token,
        }
        return response


class RefreshTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token is None:
            raise exceptions.AuthenticationFailed(
                'Учетные данные для аутентификации не были предоставлены.'
            )

        payload = token.get_jwt_payload(refresh_token)
        if payload is None:
            raise exceptions.AuthenticationFailed(
                'Невалидный токен. Войдите снова',
            )

        user_obj = user.get_user_by_email(payload.get('email'))
        if user_obj is None:
            raise exceptions.AuthenticationFailed('Пользователь не найден.')

        if not user_obj.is_active:
            raise exceptions.AuthenticationFailed('Пользователь неактивен.')

        access_token = token.generate_access_token(user_obj.email)
        return Response({'access_token': access_token})
