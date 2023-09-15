from django.urls import path

from applications.channels import views

urlpatterns = [
    path(
        'message/',
        views.MessageView.as_view(),
        name='message',
    ),
    path(
        'channel/',
        views.ChannelListViewSet.as_view(
            {
                'get': 'list',
                'post': 'create'
            }
        ),
        name='channel',
    ),
    path(
        'channel/<str:unique_hash>',
        views.ChannelDetailAPIView.as_view(),
        name='channel-detail',
    ),
    path(
        'add/<str:token>',
        views.add_user_to_channel,
        name='add_to_close_channel',
    ),
]
