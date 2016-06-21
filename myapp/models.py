from __future__ import unicode_literals

from django.db import models

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
			'Reader': (Permission.BROWSE |
					   Permission.BORROW, True),
			'Moderator': (Permission.BROWSE |
						  Permission.BORROW |
						  Permission.READER_MANAGE |
						  Permission.BOOK_MANAGE, False),
			'Administer': (0xff, False),
		}
		for r in roles:
			role = Role.objects.filter(RoleName=r)
			print role
			role = Role(RoleName=r)
			role.permissions = roles[r][0]
			role.default = roles[r][1]
			role.save()

	def __unicode__(self):
		return self.name

class User(models.Model):
	UserID = models.CharField(max_length=10, primary_key=True)
	RoleName = models.ForeignKey(Role, default="读者")
	email = models.EmailField(unique=True, db_index=True)
	password = models.CharField(max_length=30)
	UserName = models.CharField(max_length=30, null=True)
	UserSex = models.CharField(max_length=1, null=True)
	UserPhone = models.CharField(max_length=11, null=True)
	UserAddr = models.CharField(max_length=254, null=True)
	RegisterDate = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.name

class Token(models.Model):
    token = models.CharField('token', max_length=50, unique=True, db_index=True)
    user = models.OneToOneField(User)
    LastTime = models.DateTimeField(auto_now=True)
    expire = models.BigIntegerField('expire')

    def __unicode__(self):
        return self.token