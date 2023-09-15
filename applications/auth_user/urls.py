from django.urls import path
from django.views.generic import TemplateView

from applications.auth_user import views

urlpatterns = [
    path(
        'auth/',
        TemplateView.as_view(
            template_name='auth.html'
        )
    ),
    path(
        'api/auth/send-email/',
        views.send_auth_email,
        name='auth-email',
    ),
    path(
        'api/auth/login/<str:unique_hash>',
        views.login_user,
        name='login',
    ),
    path(
        'api/auth/refresh',
        views.refresh_token_view,
        name='refresh',
    ),

]
