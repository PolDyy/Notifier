from rest_framework.authentication import BaseAuthentication
from django.middleware.csrf import CsrfViewMiddleware
from rest_framework import exceptions
from applications.auth_user.models import CustomUser
from services.token.token import get_jwt_payload


class CSRFCheck(CsrfViewMiddleware):
    def _reject(self, request, reason):
        return reason


class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):

        user = CustomUser
        authorization_header = request.headers.get('Authorization')

        if not authorization_header:
            return None
        try:
            access_token = authorization_header.split(' ')[1]
        except IndexError:
            raise exceptions.AuthenticationFailed('Token prefix missing')
        payload = get_jwt_payload(access_token)
        if payload is None:
            raise exceptions.AuthenticationFailed('Access_token expired')
        user = user.objects.filter(email=payload['email']).first()
        if user is None:
            raise exceptions.AuthenticationFailed('User not found')

        if not user.is_active:
            raise exceptions.AuthenticationFailed('user is inactive')

        self.enforce_csrf(request)
        return user, None

    def _dummy_response(self, request):
        return None

    def enforce_csrf(self, request):
        check = CSRFCheck(self._dummy_response)
        check.process_request(request)
        reason = check.process_view(request, None, (), {})
        if reason:
            raise exceptions.PermissionDenied('CSRF Failed: %s' % reason)
