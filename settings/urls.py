from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path


urlpatterns = [
    path(
        'admin/',
        admin.site.urls,
    ),
    path(
        '',
        include('applications.main.urls'),
    ),
    path(
        'api/auth/',
        include('applications.auth_user.urls'),
    ),
    path(
        'api/channels/',
        include('applications.channels.urls'),
    ),
]

urlpatterns += staticfiles_urlpatterns() + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
