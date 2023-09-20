from django.urls import path

from applications.channels import views

urlpatterns = [
    path(
        'message/<str:unique_hash>',
        views.MessageViewSet.as_view(
            {
                'get': 'list',
            },
        ),
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
        views.ChannelDetailViewSet.as_view(
            {
                'get': 'retrieve',
                'patch': 'partial_update',
            }
        ),
        name='channel-detail',
    ),
    path(
        'add/<str:unique_hash>',
        views.AddUserToChannelViewSet.as_view(
            {
                'patch': 'partial_update',
            }
        ),
        name='add_to_close_channel',
    ),
]
