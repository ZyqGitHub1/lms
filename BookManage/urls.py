from django.contrib import admin
from django.views.generic import TemplateView
from django.conf.urls import *
import views

urlpatterns = [
    url(r'^allBook$', views.allBook),
    url(r'^addBook$', views.addBook),
    url(r'^deleteBook$', views.deleteBook),
    url(r'^updateBook$', views.updateBook),
    url(r'^borrowBook$', views.borrowBook),
    url(r'^returnBook$', views.returnBook),
]