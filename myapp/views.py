# -*- coding: utf-8 -*-
from django.shortcuts import render
from models import *
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from VerificationEmail import send_verificationEmail
from django.core.mail import send_mail
import datetime
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


def register(request):
	try:
		data = json.loads(request.body)
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
			send_verificationEmail(email)
			user.save()
			result = {
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
			'msg': e.args,
			},
		}
	finally:
		return HttpResponse(json.dumps(result), content_type="application/json")

def confirm(request):
	try:
		data = request.GET.get('confirm')
		s = Serializer('SECRET_KEY')
		confirm = s.loads(data)
		email = confirm['confirm']
		user = User()
		user = User.objects.filter(email=email).first()
		if user:
			user.confirmed = True
			user.save()
			confirm_msg = '您的邮箱已验证成功,将为您跳转到登录页面'
	except Exception, e:
		confirm_msg = '该链接无效或已失效,一封新的确认邮件已经发送至您的邮箱'
		# data = request.GET.get('confirm')
		# s = Serializer('SECRET_KEY')
		# confirm = s.loads(data)
		# email = confirm['confirm']
		# send_verificationEmail(email)
		print e.args
	finally:
		return render(request, 'trans.html',
				{
					'confirm_msg': confirm_msg
				})

def reconfirm(request):
	try:
		request.GET.get('email')
		send_verificationEmail(email)
		return render(request, 'trans.html',
				{
					'confirm_msg': '一封新的确认邮件已经发送至您的邮箱'
				})
	except Exception, e:
		print e.args

def login(request):
	try:
		data = json.loads(request.body)
		print data
		email = data['user']['email']
		print email
		password = data['user']['password']
		print password
		customerUser = User()
		customerUser = User.objects.filter(email=email).first()
		if not customerUser:
			raise myError("该用户不存在")
		if(check_password(password, customerUser.password)):
			token = Token()
			token = Token.objects.filter(user=customerUser)
			if(len(token) != 0):
				token.delete()
		else:
			raise myError('登录名或密码错误')
		confirmed = customerUser.confirmed
		RoleName = customerUser.role.RoleName
		customerToken = ''.join(random.sample(string.ascii_letters + string.digits, 30))
		token = Token()
		token.token = customerToken
		token.user = customerUser
		token.expire = '-1'
		token.save()
		result = {
			'data': {
				'confirmed': confirmed,
				'role_name': RoleName,
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
				'msg': e.args
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
				'msg': e.args
			}
		}
	finally:
		return HttpResponse(json.dumps(result), content_type='application/json')

def info(request):
	try:
		data = json.loads(request.body)
		print data
		token = Token()
		token = Token.objects.get(token=data['token'])
		customerUser = User()
		customerUser = token.user
		result = {
			'user': {
				'user_id': customerUser.UserID,
				'user_name': customerUser.UserName,
				'role_name': customerUser.role.RoleName,
				'email': customerUser.email,
				'sex': customerUser.UserSex,
				'phone': customerUser.UserPhone,
				'addr': customerUser.UserAddr,
				'max_borrow': customerUser.MaxBorrowNumber,
				'borrow_number': customerUser.BorrowNumber,
				'register_time': str(customerUser.RegisterDate),
				'fine': customerUser.Fine,
			},
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
				'msg': e.args
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
			send_verificationEmail(email)
		if 'user_sex' in data['user']:
			user.UserSex = data['user']['user_sex']
		if 'phone' in data['user']:
			user.UserPhone = data['user']['phone']
		if 'addr' in data['user']:
			user.UserAddr = data['user']['addr']
		if 'user_sex' in data['user']:
			user.UserSex = data['user']['user_sex']
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
				'msg': e.args,
			}
		}
	finally:
		return HttpResponse(json.dumps(result), content_type='application/json')

def borrowNow(request):
	try:
		data = json.loads(request.body)
		user = User()
		token = Token()
		token = Token.objects.get(token=data['token'])
		user = token.user
		borrowInfo = BorrowInfo()
		borrowInfo = BorrowInfo.objects.filter(reader=user)
		borrowList = []
		for borrow in borrowInfo:
			ahead_of_time = False
			if datetime.date.today() > borrow.BackTime:
				ahead_of_time = True
			book = Book()
			book = borrow.book
			if not book.BookClass:
				bookClass = None
			else:
				bookClass = book.BookClass.ClassName
			borrowList.append({
				'book_id': book.BookID,
				'book_name': book.BookName,
				'book_class': bookClass,
				'book_writer': book.BookWriter,
				'book_publish': book.BookPublish,
				'book_rno': book.BookRNo,
				'borrow_time': str(borrow.BorrowTime),
				'back_time': str(borrow.BackTime),
				'ahead_of_time': ahead_of_time,
				})
		result = {
			'successful': True,
			'data': borrowList,
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
				'id': '',
				'msg': e.args,
			}
		}
	finally:
		return HttpResponse(json.dumps(result), content_type='application/json')

def renew(request):
	try:
		data = json.loads(request.body)
		BookID = data['book']['book_id']
		token = Token()
		user = User()
		borrowInfo = BorrowInfo()
		token = Token.objects.filter(token=data['token']).first()
		user = token.user
		book = Book.objects.filter(BookID=BookID).first()
		borrowInfo = BorrowInfo.objects.filter(book=book).first()
		if borrowInfo.RenewState:
			raise myError('每本书只能续借一次')
		borrowInfo.BackTime += datetime.timedelta(15)
		borrowInfo.RenewState = True
		borrowInfo.save()
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
				'id': '',
				'msg': e.args,
			}
		}
	finally:
		return HttpResponse(json.dumps(result), content_type='application/json')