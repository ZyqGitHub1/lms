# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.db import models
import time
import datetime
import random

# Create your models here.

class Permission:
	BROWSE = 0x01
	BORROW = 0x02
	READER_MANAGE = 0x04
	BOOK_MANAGE = 0x08
	ADMINISTER = 0x80

class Role(models.Model):
	RoleName = models.CharField(max_length=30, unique=True)
	default = models.BooleanField(default=False, db_index=True)
	permissions = models.IntegerField()

	@staticmethod
	def insert_roles():
		roles = {
			'读者': (Permission.BROWSE |
					   Permission.BORROW, True),
			'协管员': (Permission.BROWSE |
						  Permission.BORROW |
						  Permission.READER_MANAGE |
						  Permission.BOOK_MANAGE, False),
			'管理员': (0xff, False),
		}
		for r in roles:
			role = Role.objects.filter(RoleName=r)
			role = Role(RoleName=r)
			role.permissions = roles[r][0]
			role.default = roles[r][1]
			role.save()

	def __unicode__(self):
		return self.RoleName
	def __str__(self):
		return self.RoleName

class User(models.Model):
	UserID = models.CharField(max_length=10, primary_key=True)
	RoleName = models.ForeignKey(Role, to_field='RoleName', default='读者')
	email = models.EmailField(unique=True, db_index=True)
	password = models.CharField(max_length=255)
	UserName = models.CharField(max_length=30, null=True, blank=True)
	MaxBorrowNumber = models.IntegerField(default=15)
	BorrowNumber = models.IntegerField(default=0)
	UserSex = models.CharField(max_length=1, null=True, blank=True)
	UserPhone = models.CharField(max_length=11, null=True, blank=True)
	UserAddr = models.CharField(max_length=255, null=True, blank=True)
	RegisterDate = models.DateTimeField(auto_now_add=True)
	Fine = models.IntegerField(default=0)
	confirmed = models.BooleanField(default=False)

	def __unicode__(self):
		return self.name

class Token(models.Model):
    token = models.CharField('token', max_length=50, unique=True, db_index=True)
    user = models.OneToOneField(User)
    LastTime = models.DateTimeField(auto_now=True)
    expire = models.BigIntegerField('expire')

    def __unicode__(self):
        return self.token

class Book(models.Model):
	BookID = models.CharField(max_length=10, primary_key=True)
	BookNo = models.CharField(max_length=11, unique=True)
	BookName = models.CharField(max_length=30)
	BookWriter = models.CharField(max_length=30)
	BookPublish = models.CharField(max_length=30)
	BookPrice = models.IntegerField()
	BookDate = models.DateField(null=True, blank=True)
	BookClass = models.CharField(max_length=30, null=True, blank=True)
	BookMain = models.TextField(null=True, blank=True)
	BookPrim = models.CharField(max_length=255, null=True, blank=True)
	BookState = models.BooleanField(default=True)
	BookRNo = models.CharField(max_length=30)

	def __unicode__(self):
		return self.BookID

class BorrowInfo(models.Model):
	BookID = models.OneToOneField(Book, primary_key=True)
	ReaderID = models.OneToOneField(User)
	BorrowTime = models.DateTimeField(auto_now_add=True)
	BackTime = models.DateTimeField()


class FineInfo(models.Model):
	BookID = models.OneToOneField(Book, primary_key=True)
	ReaderID = models.OneToOneField(User)
	Fine = models.IntegerField()