import logging
from django.contrib.auth import get_user_model
from django.db.models import Q
from account import models
from account.models import GroupSubcategory, Category, SubCategory

User = get_user_model()


logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG,
                    filename=u'erp.log')


def get_user_info(user_data):
    user = user_data.get("user")
    user_obj = User.objects.get(id=user['id'])

    user_data["roles"] = list(user_obj.groups.values('id', 'name'))

    categorys_data = get_user_categorys_data2(user_obj)

    return {
        "categories": categorys_data,
        "user": user_data
    }


def get_user_accept_subcategorys(user):
    subcategorys_set = set()
    for group in user.groups.all():
        if GroupSubcategory.objects.filter(group=group).exists():
            subcategorys = set(GroupSubcategory.objects.get(group=group).links.exclude(status=3).order_by('priority'))
            subcategorys_set = subcategorys_set.union(subcategorys)

    return subcategorys_set


def get_user_categorys_data(user):
    temp = {}

    subcategorys = get_user_accept_subcategorys(user)

    for subcategory in subcategorys:
        category = subcategory.get_category()
        if category:
            if not temp.get(category.name):
                temp[category.name] = category.get_data()
                temp[category.name]["links"] = list()

            temp[category.name]["links"].append(subcategory.get_data())

    result = sorted([temp[key] for key in temp], key=lambda k: k['priority'])
    if result:
        return result
    return None


def get_subcategory(link):
    sub_cat = SubCategory.objects.filter(link=link)

    if sub_cat.exists():
        return sub_cat[0]

    return None



