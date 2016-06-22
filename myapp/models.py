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
		return self.name

class User(models.Model):
	UserID = models.CharField(max_length=10, primary_key=True)
	RoleName = models.ForeignKey(Role, to_field='RoleName', default='读者')
	email = models.EmailField(unique=True, db_index=True)
	password = models.CharField(max_length=255)
	UserName = models.CharField(max_length=30, null=True)
	MaxBorrow = models.IntegerField(default=15)
	UserSex = models.CharField(max_length=1, null=True)
	UserPhone = models.CharField(max_length=11, null=True)
	UserAddr = models.CharField(max_length=255, null=True)
	RegisterDate = models.DateTimeField(auto_now_add=True)
	Fine = models.IntegerField(default=0)
	confirmed = models.BooleanField(default=False)

	def __unicode__(self):
		return self.name

class Token(models.Model):
    token = models.CharField('token', max_length=50, unique=True, db_index=True)
    user = models.OneToOneField(User)
    LastTime = models.DateTimeField(auto_now=True)
    VerificationCode = models.CharField(max_length=6, null=True)
    CodeTime = models.CharField(max_length=30, null=True)
    expire = models.BigIntegerField('expire')

    def get_verification_code(self):
 		code_list = []
 		for i in range(2):
  			random_num = random.randint(0, 9)
  			a = random.randint(65, 90)
  			b = random.randint(97, 122)
  			random_uppercase_letter = chr(a)
  			random_lowercase_letter = chr(b)
  			code_list.append(str(random_num))
  			code_list.append(random_uppercase_letter)
  			code_list.append(random_lowercase_letter)
 		verification_code = ''.join(code_list)
 		return verification_code

    def get_now(self):
    	return time.mktime(datetime.datetime.now().timetuple())

    def __unicode__(self):
        return self.token