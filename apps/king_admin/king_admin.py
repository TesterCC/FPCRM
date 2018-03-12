#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'MFC'
__time__ = '18/3/12 01:51'

from crm import models

enabled_admins = {}


class BaseAdmin(object):
    list_display = []
    list_filter = []


class CustomAdmin(BaseAdmin):
    list_display = ['qq', 'name']
    # model = models.Customer


class CustomerFollowUpAdmin(BaseAdmin):
    list_display = ('customer', 'consultant', 'date')


def register(model_class, admin_class=None):
    if model_class._meta.app_label not in enabled_admins:
        enabled_admins[model_class._meta.app_label] = {}

    # admin_obj = admin_class()   # obj可以传回前端做渲染
    admin_class.model = model_class    # 绑定model对象和admin类，相当于增加新属性
    enabled_admins[model_class._meta.app_label][model_class._meta.model_name] = admin_class


register(models.Customer, CustomAdmin)
register(models.CustomerFollowUp, CustomerFollowUpAdmin)

# print(enabled_admins)
# {'crm': {'customer': <class 'king_admin.king_admin.CustomAdmin'>, 'customerfollowup': <class 'king_admin.king_admin.CustomerFollowUpAdmin'>}}