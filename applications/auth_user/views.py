from rest_framework.request import Request
from applications.auth_user.serializers import AuthSerializer
from services.smtp.smtp import EmailSending
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from services.token.token import generate_access_token, generate_refresh_token, get_jwt_payload
from services.hash.hash import get_hash_value
from services.users.user import create_user_if_not_exists, get_user_by_email
from django.views.decorators.csrf import ensure_csrf_cookie


@api_view(['POST'])
@permission_classes([AllowAny])
def send_auth_email(request: Request) -> Response:
    data = request.data
    serializer = AuthSerializer(data=data)
    if serializer.is_valid():
        EmailSending.send_auth_email(data.get('email'))
        return Response(
            {
                'success': True,
                'message': 'Ссылка для входа отправлена на почту'
            }
        )
    return Response(
        {
            'success': False,
            'message': 'Проверьте правильность заполнения формы.',
        }
    )


@api_view(['GET'])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def login_user(request: Request, unique_hash: str) -> Response: # hash
    email = get_hash_value(unique_hash)
    print(email)
    if not email or not isinstance(email, str):
        raise exceptions.AuthenticationFailed(
            'Невалидная ссылка авторизации',
        )
    create_user_if_not_exists(email)
    access_token = generate_access_token(email)
    refresh_token = generate_refresh_token(email)
    response = Response()
    response.set_cookie(key='refresh_token', value=refresh_token, httponly=True)
    response.data = {
        'access_token': access_token,
    }
    return response


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token_view(request: Request):

    refresh_token = request.COOKIES.get('refresh_token')
    if refresh_token is None:
        raise exceptions.AuthenticationFailed(
            'Учетные данные для аутентификации не были предоставлены.'
        )
    payload = get_jwt_payload(refresh_token)
    if payload is None:
        raise exceptions.AuthenticationFailed(
            'Невалидный токен. Войдите снова',
        )

    user = get_user_by_email(payload.get('email'))
    if user is None:
        raise exceptions.AuthenticationFailed('Пользователь не найден.')

    if not user.is_active:
        raise exceptions.AuthenticationFailed('Пользователь неактивен.')

    access_token = generate_access_token(user)
    return Response({'access_token': access_token})
