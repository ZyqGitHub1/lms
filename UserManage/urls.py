# -*- coding:utf-8 -*-
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf.urls import *
import views

urlpatterns = [
    url(r'^allUser$', views.allUser),
    url(r'^addUser$', views.addUser),
    url(r'^updateUserInfo$', views.updateUserInfo),
    url(r'^deleteUser$', views.deleteUser),
    url(r'^addAdministrators$', views.addAdministrators),
    url(r'^deleteAdministrators$', views.deleteAdministrators),
]