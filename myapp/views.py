# -*- coding: utf-8 -*-
from django.shortcuts import render
from models import *
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password
from VerificationEmail import send_verificationEmail
import json
import simplejson
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


def register(request):
	try:
		print request.body
		data = simplejson.loads(request.body)
		email = data['user']['email']
		password = data['user']['password']
		repassword = data['user']['repassword']
		existUser = User.objects.filter(email=email).first()
		if existUser:
			raise myError('该邮箱已被注册!')
		if (password == repassword):
			lastUser = User.objects.all().last()
			userID = str(int(lastUser.UserID) + 1)
			user = User()
			user.password = make_password(password)
			user.UserID = userID
			user.email = email
			user.save()
			token = Token()
			token.user = user
			token.expire = -1
			VerificationCode = token.get_verification_code()
			token.VerificationCode = VerificationCode
			token.CodeTime = token.get_now()
			token.save()
			send_verificationEmail(email, VerificationCode)
			result = {
			'successful': True,
			'error': {
				'id': '',
				'msg': '',
				},
			}
	except Exception,e:
		result = {
		'successful': False,
		'error': {
			'id': '1024',
			'msg': e.args,
			},
		}
	finally:
		return HttpResponse(json.dumps(result), content_type="application/json")

def login(request):
	try:
		data = json.loads(request.body)
		email = data['user']['email']
		password = data['user']['password']
		customerUser = User()
		customerUser = User.objects.filter(email=email).first()
		if not customerUser:
			raise myError("该邮箱还未注册，不能登陆!")
		if(check_password(password, customerUser.password)):
			token = Token()
			token = Token.objects.filter(user=customerUser).first()
			if(len(token) != 0):
				token.delete()
		else:
			raise myError('登录名或密码错误!')
		customerToken = ''.join(random.sample(string.ascii_letters + string.digits, 30))
		token = Token()
		token.token = customerToken
		token.user = customerUser
		token.expire = '-1'
		token.save()
		result = {
			'data': {
				'token': customerToken,
				'expire': -1,
			},
			'successful': True,
			'error': {
				'id': '',
				'msg': '',
			},
		}
	except myError, e:
		result = {
			'successful': False,
			'error': {
				'id': '1',
				'msg': e.value
			}
		}
	except Exception,e:
		result = {
			'successful': False,
			'error': {
				'id': '1024',
				'msg': e.value
			}
		}
	finally:
		return HttpResponse(json.dumps(result), content_type='application/json')

def logout(request):
	try:
		data = json.loads(request.body)
		customerToken = data['token']
		token = Token()
		token = Token.objects.get(token=customerToken)
		token.delete()
		result = {
			'successful': True,
			'error': {
				'id': '',
				'msg': '',
			},
		}
	except Exception as e:
		result = {
			'successful': False,
			'error': {
				'id': '1024',
				'msg': e.value
			}
		}
	finally:
		return HttpResponse(json.dumps(result), content_type='application/json')

def info(request):
	try:
		data = json.loads(request)
		token = Token()
		token = Token.objects.get(token=data['token'])
		customerUser = User()
		customerUser = token.user
		result = {
			'user': {
				'user_id': customerUser.UserID,
				'user_name': customerUser.UserName,
				'role_name': customerUser.role_name,
				'email': customerUser.email,
				'sex': customerUser.UserSex,
				'phone': customerUser.UserPhone,
				'addr': customerUser.UserAddr,
				'register_time': customerUser.RegisterTime,
				'max_borrow': customerUser.MaxBorrow,
				'fine': customerUser.Fine,
			},
			'successful': True,
			'error': {
				'id': '',
				'msg': '',
			}
		}
	except Exception, e:
		result = {
			'successful': False,
			'error': {
				'id': '1024',
				'msg': e.value
			}
		}
	finally:
		return HttpResponse(json.dumps(result), content_type='application/json')

def change_info(request):
	try:
		data = json.loads(request.body)
		user = User()
		token = Token()
		token = Token.objects.get(token=data['token'])
		user = token.user
		if 'user_name' in data['user']:
			user.UserName = noneIfEmptyString(data['user']['user_name'])
		if 'email' in data['user']:
			email = data['user']['email']
			existUser = User.objects.get(email=email)
			if existUser:
				raise myError('该邮箱已被注册!')
			user.email = email
		if 'user_sex' in data['user']:
			user.UserSex = data['user']['user_sex']
		if 'role_name' in data['user']:
			user.RoleName = data['user']['role_name']
		if 'max_borrow' in data['user']:
			user.MaxBorrow = data['user']['max_borrow']
		if 'phone' in data['user']:
			user.UserPhone = data['user']['phone']
		if 'addr' in data['user']:
			user.UserAddr = data['user']['addr']
		if 'fine' in data['user']:
			user.Fine = data['user']['fine']
		user.save()
		result = {
			'successful': True,
			'error': {
				'id': '',
				'msg': '',
			}
		}
	except Exception, e:
		result = {
			'successful': False,
			'error': {
				'id': '1024',
				'msg': e.value,
			}
		}
	finally:
		return HttpResponse(json.dumps(result), content_type='application/json')

def change_password(request):
	try:
		data = json.loads(request.body)
		user = User()
		token = Token()
		token = Token.objects.get(token=data['token'])
		user = token.user
		if(not check_password(data['user']['old_password'],user.password)):
			raise myError('原密码输入错误!')

		user.password = make_password(data['user']['new_password'])
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
				'msg': e.value,
			}
		}
	finally:
		return HttpResponse(json.dumps(result), content_type='application/json')