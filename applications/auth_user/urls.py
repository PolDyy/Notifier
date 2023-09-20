from django.urls import path

from applications.auth_user import views

urlpatterns = [
    path(
        'send-email/',
        views.SendAuthEmailView.as_view(),
        name='auth-email',
    ),
    path(
        'login/<str:unique_hash>',
        views.LoginUserView.as_view(),
        name='login',
    ),
    path(
        'refresh/',
        views.RefreshTokenView.as_view(),
        name='refresh',
    ),

]
