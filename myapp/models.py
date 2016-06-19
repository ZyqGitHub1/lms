from __future__ import unicode_literals

from django.db import models

# Create your models here.

class User(models.Model):
	name = models.CharField(max_length=30, unique=True, db_index=True)
	password = models.CharField(max_length=30)
	email = models.EmailField('email')

	def __unicode__(self):
		return self.name

class Token(models.Model):
    token = models.CharField('token', max_length=50, unique=True, db_index=True)
    user = models.OneToOneField(User)
    expire = models.BigIntegerField('expire')

    def __unicode__(self):
        return self.token