# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.shortcuts import render
from myapp.models import *
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password
from myapp.VerificationEmail import send_verificationEmail
import json
import random
import string
# Create your views here.

def noneIfEmptyString(value):
    if value == "":
        return None
    return value
def noneIfNoKey(dict, key):
    if key in dict:
        value = dict[key]
        if value == "":
            return None
        return value
    return None

class myError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def allUser(request):
	try:
		data = json.loads(request.body)
		token = Token()
		token = Token.objects.filter(token=data['token']).first()
		user = User()
		user = token.user
		if (user.role.RoleName != '管理员' and user.role.RoleName != '协管员'):
			raise myError('对不起,您没有该权限!')
		users = User.objects.all()
		userList = []
		for user in users:
			userList.append({
				'user_id': user.UserID,
				'role_name': user.role.RoleName,
				'user_email': user.email,
				'user_name': user.UserName,
				'user_maxborrow': user.MaxBorrowNumber,
				'user_borrow': user.BorrowNumber,
				'user_sex': noneIfEmptyString(user.UserSex),
				'user_phone': noneIfEmptyString(user.UserPhone),
				'user_addr': noneIfEmptyString(user.UserAddr),
				'user_registerdate': str(user.RegisterDate),
				'user_fine': user.Fine,
				'user_totalborrow': user.TotalBorrow,
				'user_confirmed': user.confirmed
				})
		result = {
			'successful': True,
			'data': userList,
			'error': {
				'id': '',
				'msg': '',
			}
		}
	except myError, e:
		result = {
			'successful': False,
			'error': {
				'id': '',
				'msg': e.value,
			}
		}
	except Exception, e:
		result = {
			'successful': False,
			'error': {
				'id': '',
				'msg': e.args,
			}
		}
	finally:
		return HttpResponse(json.dumps(result), content_type='application/json')

def addUser(request):
	try:
		data = json.loads(request.body)
		token = Token()
		token = Token.objects.filter(token=data['token']).first()
		user = User()
		user = token.user
		if (user.role.RoleName != '管理员' and user.role.RoleName != '协管员'):
			raise myError('对不起,您没有该权限!')
		user = User()
		lastUser = User.objects.all().last()
		UserID = str(int(lastUser.UserID) + 1)
		user.UserID = UserID
		role = Role.objects.filter(RoleName=data['user']['role_name']).first()
		user.role = role
		user.password = make_password(data['user']['new_password'])
		email = data['user']['user_email']
		existUser = User.objects.filter(email=email).first()
		if existUser:
			raise myError('该邮箱已被注册!')
		user.email = email
		if 'user_name' in data['user']:
			user.UserName = noneIfEmptyString(data['user']['user_name'])
		if 'user_sex' in data['user']:
			user.UserSex = data['user']['user_sex']
		if 'role_name' in data['user']:
			role = Role.objects.filter(RoleName=data['user']['role_name']).first()
			user.role = role
		if 'max_borrow' in data['user']:
			user.MaxBorrow = data['user']['max_borrow']
		if 'phone' in data['user']:
			user.UserPhone = data['user']['phone']
		if 'addr' in data['user']:
			user.UserAddr = data['user']['addr']
		user.confirmed = True
		user.save()
		result = {
			'successful': True,
			'error': {
				'id': '',
				'msg': '',
			}
		}
	except myError, e:
		result = {
			'successful': False,
			'error': {
				'id': '1024',
				'msg': e.value,
			}
		}
	except Exception, e:
		result = {
			'successful': False,
			'error': {
				'id': '',
				'msg': e.args,
			}
		}
	finally:
		return HttpResponse(json.dumps(result), content_type='application/json')

def updateUserInfo(request):
	try:
		data = json.loads(request.body)
		token = Token()
		token = Token.objects.filter(token=data['token']).first()
		user = User()
		user = token.user
		if (user.role.RoleName != '管理员' and user.role.RoleName != '协管员'):
			raise myError('对不起,您没有该权限!')
		UserID = data['user']['user_id']
		user = User.objects.filter(UserID=UserID).first()
		if 'user_name' in data['user']:
			user.UserName = noneIfEmptyString(data['user']['user_name'])
		if 'new_password' in data['user']:
			user.password = make_password(data['user']['new_password'])
		if 'email' in data['user']:
			email = data['user']['email']
			existUser = User.objects.filter(email=email).first()
			if existUser:
				raise myError('该邮箱已被注册!')
			user.email = email
			send_verificationEmail(email)
		if 'user_sex' in data['user']:
			user.UserSex = data['user']['user_sex']
		if 'role_name' in data['user']:
			role = Role.objects.filter(RoleName=data['user']['role_name']).first()
			user.role = role
		if 'max_borrow' in data['user']:
			user.MaxBorrow = data['user']['user_maxborrow']
		if 'phone' in data['user']:
			user.UserPhone = data['user']['user_phone']
		if 'addr' in data['user']:
			user.UserAddr = data['user']['user_addr']
		if 'fine' in data['user']:
			user.Fine = data['user']['user_fine']
		if 'total_borrow' in data['user']:
			user.TotalBorrow = data['user']['user_totalborrow']
		user.save()
		result = {
			'successful': True,
			'error': {
				'id': '',
				'msg': '',
			}
		}
	except myError, e:
		result = {
			'successful': False,
			'error': {
				'id': '1',
				'msg': e.value
			}
		}
	except Exception, e:
		result = {
			'successful': False,
			'error': {
				'id': '1024',
				'msg': e.args,
			}
		}
	finally:
		return HttpResponse(json.dumps(result), content_type='application/json')


def deleteUser(request):
	try:
		data = json.loads(request.body)
		token = Token()
		token = Token.objects.filter(token=data['token']).first()
		user = User()
		user = token.user
		if (user.role.RoleName != '管理员' and user.role.RoleName != '协管员'):
			raise myError('对不起,您没有该权限!')
		dUserID = data['user']['user_id']
		dUser = User()
		dUser = User.objects.filter(UserID=dUserID).first()
		if not dUser:
			raise myError('该用户不存在!')
		if dUser.role.RoleName == '管理员':
			raise myError('对不起,您没有该权限!')
		if dUser.role.RoleName == '协管员' and User.role.RoleName != '管理员':
			 raise myError('对不起,您没有该权限!')
		dUser.delete()
		result = {
			'successful': True,
			'error': {
				'id': '',
				'msg': ''
			}
		}
	except myError, e:
		result = {
			'successful': False,
			'error': {
				'id': '3',
				'msg': e.value,
			}
		}
	except Exception, e:
		result = {
			'successful': False,
			'error': {
				'id': '1024',
				'msg': e.args,
			}
		}
	finally:
		return HttpResponse(json.dumps(result), content_type='application/json')

def addAdministrators(request):
	try:
		data = json.loads(request.body)
		token = Token()
		token = Token.objects.filter(token=data['token']).first()
		user = User()
		user = token.user
		if (user.role.RoleName != '管理员'):
			raise myError('对不起,您没有该权限!')
		UserID = data['user']['user_id']
		user = User.objects.filter(UserID=UserID).first()
		role = Role.objects.filter(RoleName='协管员').first()
		user.role = role
		user.save()
		result = {
			'successful': True,
			'error': {
				'id': '',
				'msg': ''
			}
		}
	except myError, e:
		result = {
			'successful': False,
			'error': {
				'id': '3',
				'msg': e.value,
			}
		}
	except Exception, e:
		result = {
			'successful': False,
			'error': {
				'id': '1024',
				'msg': e.args,
			}
		}
	finally:
		return HttpResponse(json.dumps(result), content_type='application/json')

def deleteAdministrators(request):
	try:
		data = json.loads(request.body)
		token = Token()
		token = Token.objects.filter(token=data['token']).first()
		user = User()
		user = token.user
		if str(user.role.RoleName) != '管理员':
			raise myError('对不起,您没有该权限!')
		UserID = data['user']['user_id']
		user = User.objects.filter(UserID=UserID).first()
		role = Role.objects.filter(RoleName='读者').first()
		user.role = role
		user.save()
		result = {
			'successful': True,
			'error': {
				'id': '',
				'msg': ''
			}
		}
	except myError, e:
		result = {
			'successful': False,
			'error': {
				'id': '3',
				'msg': e.value,
			}
		}
	except Exception, e:
		result = {
			'successful': False,
			'error': {
				'id': '1024',
				'msg': e.args,
			}
		}
	finally:
		return HttpResponse(json.dumps(result), content_type='application/json')
