from django.shortcuts import render

import importlib

# Create your views here.
from king_admin import king_admin


def index(request):
    """
    Render king admin index page
    :param request:
    """
    # print(king_admin.enabled_admins['crm']['customer'].model)    # <class 'crm.models.Customer'>
    return render(request, "king_admin/table_index.html", {
        'table_list': king_admin.enabled_admins
    })


def display_table_objs(request, app_name, table_name):
    """
    display each table objs
    """
    print("-->", app_name, table_name)
    # model_module = importlib.import_module('%s.models' % app_name)   # 'crm.models'
    # model_obj = getattr(model_module, table_name)   # 遍历出来的表名是小写，报错，粗暴办法，遍历比对

    admin_class = king_admin.enabled_admins[app_name][table_name]

    return render(request, "king_admin/table_objs.html", {
        "admin_class": admin_class
    })






