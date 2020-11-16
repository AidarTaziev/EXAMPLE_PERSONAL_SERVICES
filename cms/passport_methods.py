import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from account.models import GroupSubcategory


User = get_user_model()


def get_user_from_passport(user_id=None, session_id=None):
    data = {
        'session_id': session_id,
        'user_id': user_id,
        'secret': settings.PASSPORT_SECRET_KEY,
    }
    try:
        response = requests.post("{passport_url}/auth/data".format(passport_url=settings.PASSPORT_URL), data=data)
    except requests.exceptions.RequestException as e:
        return None

    if response.status_code == 200:
        data = response.json()
        if not data['error']:
            sync_user(data['data']['user'])
            return data['data']

    return None


def sync_user(user_dict):
    user = User.objects.filter(pk=user_dict.get("id"))
    if user.exists():
        user.update(**user_dict)
        user_instance = user[0]
    else:
        user_instance = User.objects.create(**user_dict)

    if not user_instance.groups.exists():
        group = Group.objects.get(name="Покупатель")
        user_instance.groups.add(group)
