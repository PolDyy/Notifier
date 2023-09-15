from django.core.exceptions import ObjectDoesNotExist

from applications.auth_user.models import CustomUser
from user_agents import parse


def get_user_by_email(email: str):
    try:
        user = CustomUser.objects.get(email=email)
    except ObjectDoesNotExist:
        return
    return user


def create_user_if_not_exists(email: str):
    user = get_user_by_email(email)
    if user is None:
        CustomUser.objects.create_user(email)


def update_user_device(request):
    user = request.user
    user_agent = parse(request.META.get('HTTP_USER_AGENT'))
    device = user_agent.device.family
    ip_address = request.META.get('REMOTE_ADDR')
    user.device = device
    user.ip = ip_address
    user.save()
