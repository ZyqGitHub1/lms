from django.contrib import admin
from django.views.generic import TemplateView
from django.conf.urls import *
import views

urlpatterns = [
    url(r'^allBook$', views.allBook),
    url(r'^allFreeBook$', views.allFreeBook),
    url(r'^allBorrow$', views.allBorrow),
    url(r'^allLost$', views.allLost),
    url(r'^allFine$', views.allFine),
    url(r'^addBook$', views.addBook),
    url(r'^deleteBook$', views.deleteBook),
    url(r'^updateBook$', views.updateBook),
    url(r'^borrowBook$', views.borrowBook),
    url(r'^returnBook$', views.returnBook),
    url(r'^lostFine$', views.lostFine),
    url(r'^allBookClasses$', views.allBookClasses),
    url(r'^addBookClasses$', views.addBookClasses),
]