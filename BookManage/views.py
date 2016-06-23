# -*- coding:utf-8 -*-
from django.shortcuts import render
from myapp.models import *
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
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

def allBook(requset):
	try:
		data = json.loads(requset.body)
		token = Token()
		token = Token.objects.filter(token=data['token']).first()
		user = User()
		user = token.user
		print str(user.RoleName)
		if (str(user.RoleName) != '管理员' and str(user.RoleName) != '协管员'):
			raise myError('对不起,您没有该权限!')
		books = Book.objects.all()
		bookList = []
		for book in books:
			bookList.append({
				'book_id': book.BookID,
				'book_no': book.BookNo,
				'book_name': book.BookName,
				'book_writer': book.BookWriter,
				'book_publish': book.BookPublish,
				'book_price': book.BookPrice,
				'book_date': noneIfEmptyString(str(book.BookDate)),
				'book_class': noneIfEmptyString(book.BookClass),
				'book_main': noneIfEmptyString(book.BookMain),
				'book_prim': noneIfEmptyString(book.BookPrim),
				'book_state': book.BookState,
				'book_rno': book.BookRNo,
				})
		result = {
			'successful': True,
			'data': bookList,
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


def addBook(requset):
	try:
		data = json.loads(requset.body)
		token = Token()
		token = Token.objects.filter(token=data['token'])
		user = User()
		user = token.user
		if (user.RoleName != '管理员' and user.RoleName != '协管员'):
			raise myError('对不起,您没有添加图书的权限!')
		book = Book()
		BookID = data['book']['book_id']
		existBook = Book()
		existBook = Book.objects.filter(BookID=BookID).first()
		if existBook:
			raise myError('该图书编号已存在')
		book.BookID = BookID
		BookNo = data['book']['book_no']
		book.BookNo = BookNo
		BookName = data['book']['book_name']
		book.BookName = BookName
		BookWriter = data['book']['book_writer']
		book.BookWriter = BookWriter
		BookPublish = data['book']['book_publish']
		book.BookPublish = BookPublish
		BookPrice = data['book']['book_price']
		book.BookPrice = BookPrice
		book.BookCopy = BookCopy
		BookState = data['book']['book_state']
		book.BookState = BookState
		BookRNo = data['book']['book_rno']
		book.BookRNo = BookRNo
		if 'book_data' in data['book']:
			book.BookDate = data['book']['book_data']
		if 'book_class' in data['book']:
			book.BookClass = data['book']['book_class']
		if 'book_main' in data['book']:
			book.BookMain = data['book']['book_main']
		if 'book_prim' in data['book']:
			book.BookPrim = data['book']['book_prim']
		if 'book_copy' in data['book']:
			book.BookMain = data['book']['book_copy']
		book.save()
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

def deleteBook(requset):
	try:
		data = json.loads(requset.body)
		token = Token()
		token = Token.objects.filter(token=data['token'])
		user = User()
		user = token.user
		if (user.RoleName != '管理员' and user.RoleName != '协管员'):
			raise myError('对不起,您没有删除图书的权限!')
		BookID = data['book']['book_id']
		book = Book()
		book = Book.objects.filter(BookID=BookID).first()
		if not book.BookState:
			raise myError('该书已被借出,不能删除!')
		book.delete()
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

def updateBook(requset):
	try:
		data = json.loads(requset.body)
		token = Token()
		token = Token.objects.filter(token=data['token'])
		user = User()
		user = token.user
		if (user.RoleName != '管理员' and user.RoleName != '协管员'):
			raise myError('对不起,您没有修改图书信息的权限!')
		book = Book()
		book = Book.objects.filter(BookID=BookID).first()
		if 'book_name' in data['book']:
			book.BookName = data['book']['book_name']
		if 'book_writer' in data['book']:
			book.BookWriter = data['book']['book_writer']
		if 'book_publish' in data['book']:
			book.BookPublish = data['book']['book_publish']
		if 'book_price' in data['book']:
			book.BookPrice = data['book']['book_price']
		if 'book_state' in data['book']:
			book.BookState = data['book']['book_state']
		if 'book_rno' in data['book']:
			book.BookRNo = data['book']['book_rno']
		if 'book_no' in data['book']:
			book.BookNo = data['book']['book_no']
		if 'book_class' in data['book']:
			book.BookClass = data['book']['book_class']
		if 'book_main' in data['book']:
			book.BookMain = data['book']['book_main']
		if 'book_prim' in data['book']:
			book.BookPrim = data['book']['book_prim']
		if 'book_copy' in data['book']:
			book.BookMain = data['book']['book_copy']
		book.save()
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
				'id': '',
				'msg': e.args,
			}
		}
	finally:
		return HttpResponse(json.dumps(result), content_type='application/json')

def borrowBook(requset):
	try:
		data = json.loads(requset.body)
		borrow = BorrowInfo()
		BookID = data['borrow']['book_id']
		ReaderID = data['borrow']['reader_id']
		user = User()
		user = User.objects.filter(UserID=ReaderID).first()
		if not user:
			raise myError('该用户不存在,请检查是否输入错误!')
		book = Book()
		book = Book.objects.filter(BookID=BookID).first()
		if not book:
			raise myError('该图书编号不存在,请检查是否输入错误!')
		existBorrow = BorrowInfo()
		if not book.BookState:
			raise myError('该书目前不能借出或已借出!')
		existBorrow = BorrowInfo.objects.filter(BookID=BookID).first()
		if existBorrow:
			raise myError('该书已被借出!')
		fine = FineInfo()
		fine = FineInfo.objects.filter(ReaderID=ReaderID).first()
		if fine:
			raise myError('该用户有罚款未缴纳,不能借书!')
		if user.BorrowNumber > user.MaxBorrowNumber:
			raise myError('该用户借书本数已达可借本书上限值!')
		book.BookState = False
		user.BorrowNumber += 1
		book.save()
		user.save()
		borrow.save()
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

def returnBook(requset):
	try:
		data = json.loads(requset.body)
		BookID = BookID = data['return']['book_id']
		book = Book()
		book = Book.objects.filter(BookID=BookID)
		if not book:
			raise myError('该图书编号不存在,请检查是否输入错误!')
		borrow = BorrowInfo()
		borrow = BorrowInfo.objects.filter(BookID=BookID).first()
		if not borrow:
			raise myError('不存在该借阅信息,请检查是否输入错误!')
		UserID = borrow.ReaderID
		user = User()
		user = User.objects.filter(UserID=ReaderID).first()
		user.BorrowNumber -= 1
		book_copy.save()
		borrow.delete()
		user.save()
		book.BookState = True
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
