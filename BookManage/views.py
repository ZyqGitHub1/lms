# -*- coding:utf-8 -*-
from django.shortcuts import render
from myapp.models import *
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
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

def allBook(request):
	try:
		books = Book.objects.all()
		bookList = []
		for book in books:
			if not book.BookClass:
				bookClass = None
			else:
				bookClass = book.BookClass.ClassName
			bookList.append({
				'book_id': book.BookID,
				'book_no': book.BookNo,
				'book_name': book.BookName,
				'book_writer': book.BookWriter,
				'book_publish': book.BookPublish,
				'book_price': book.BookPrice,
				'book_date': noneIfEmptyString(str(book.BookDate)),
				'book_class': noneIfEmptyString(bookClass),
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

def allFreeBook(request):
	try:
		data = json.loads(request.body)
		token = Token()
		token = Token.objects.filter(token=data['token']).first()
		user = User()
		user = token.user
		if (user.role.RoleName != '管理员' and user.role.RoleName != '协管员'):
			raise myError('对不起,您没有该权限!')
		books = Book.objects.filter(BookState=True)
		bookList = []
		for book in books:
			if not book.BookClass:
				bookClass = None
			else:
				bookClass = book.BookClass.ClassName
			bookList.append({
				'book_id': book.BookID,
				'book_no': book.BookNo,
				'book_name': book.BookName,
				'book_writer': book.BookWriter,
				'book_publish': book.BookPublish,
				'book_price': book.BookPrice,
				'book_date': noneIfEmptyString(str(book.BookDate)),
				'book_class': noneIfEmptyString(bookClass),
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

def allFine(request):
	try:
		data = data = json.loads(request.body)
		token = Token()
		token = Token.objects.filter(token=data['token']).first()
		user = User()
		user = token.user
		if (user.role.RoleName != '管理员' and user.role.RoleName != '协管员'):
			raise myError('对不起,您没有该权限!')
		fineUsers = FineInfo.objects.all()
		fineUserIDList = []
		for fineUser in fineUsers:
			fineUserIDList.append(fineUser.reader.UserID)
		fineUserIDList = list(set(fineUserIDList))
		fineList = []
		for fineUserID in fineUserIDList:
			user = User.objects.filter(UserID=fineUserID).first()
			print user.UserID
			everyList = []
			fines = FineInfo.objects.filter(reader=user)
			totalMoney = 0
			operateId = None
			if fines[0].admin:
				operateId = fines[0].admin.UserID
			for fine in fines:
				totalMoney += fine.Fine
			everyList.append({
					'user_id': user.UserID,
					'user_email': user.email,
					'pay_money': totalMoney,
					'pay_state': fine.PayState,
					'pay_date': str(fine.PayDate),
					'operate_id':  str(operateId)
					})
			for fine in fines:
				# borrowInfo = BorrowInfo.objects.filter(book=fine.book).first()
				everyList.append({
					'book_id': fine.book.BookID,
					'book_name': fine.book.BookName,
					# 'borrow_date': str(borrowInfo.BorrowTime),
					# 'back_date': str(borrowInfo.BackTime),
					'fine_money': fine.Fine,
					})
			fineList.append(everyList)
			print user.UserID
		result = {
			'successful': True,
			'data': fineList,
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

def allLost(request):
	try:
		data = data = json.loads(request.body)
		token = Token()
		token = Token.objects.filter(token=data['token']).first()
		user = User()
		user = token.user
		if (user.role.RoleName != '管理员' and user.role.RoleName != '协管员'):
			raise myError('对不起,您没有该权限!')
		losts = LostBook.objects.all()
		lostList = []
		for lost in losts:
			if not lost.book.BookClass:
				bookClass = None
			else:
				bookClass = lost.book.BookClass.ClassName
			lostList.append({
				'book_id': lost.book.BookID,
				'book_name': lost.book.BookName,
				'user_id': lost.reader.UserID,
				'pay_money': lost.PayMoney,
				'pay_date': str(lost.OperateDate),
				'admin_id': lost.admin.UserID,
				'book_writer': lost.book.BookWriter,
				'book_publish': lost.book.BookPublish,
				'book_price': lost.book.BookPrice,
				'book_date': noneIfEmptyString(str(lost.book.BookDate)),
				'book_class': noneIfEmptyString(bookClass),
				'book_main': noneIfEmptyString(lost.book.BookMain),
				'book_prim': noneIfEmptyString(lost.book.BookPrim),
				})
		result = {
			'successful': True,
			'data': lostList,
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

def allBorrow(request):
	try:
		data = data = json.loads(request.body)
		token = Token()
		token = Token.objects.filter(token=data['token']).first()
		user = User()
		user = token.user
		if (user.role.RoleName != '管理员' and user.role.RoleName != '协管员'):
			raise myError('对不起,您没有该权限!')
		borrows = BorrowInfo.objects.all()
		borrowList = []
		for borrow in borrows:
			if not borrow.book.BookClass:
				bookClass = None
			else:
				bookClass = borrow.book.BookClass.ClassName
			borrowList.append({
				'book_id': borrow.book.BookID,
				'book_name': borrow.book.BookName,
				'user_id': borrow.reader.UserID,
				'borrow_time': str(borrow.BorrowTime),
				'back_time': str(borrow.BackTime),
				'renew_state': borrow.RenewState,
				'book_no': borrow.book.BookNo,
				'book_writer': borrow.book.BookWriter,
				'book_publish': borrow.book.BookPublish,
				'book_price': borrow.book.BookPrice,
				'book_date': noneIfEmptyString(str(borrow.book.BookDate)),
				'book_class': noneIfEmptyString(bookClass),
				'book_main': noneIfEmptyString(borrow.book.BookMain),
				'book_prim': noneIfEmptyString(borrow.book.BookPrim),
				})
		result = {
			'successful': True,
			'data': borrowList,
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

def addBook(request):
	try:
		data = json.loads(request.body)
		token = Token()
		token = Token.objects.filter(token=data['token']).first()
		user = User()
		user = token.user
		print user.role.RoleName
		if (user.role.RoleName != '管理员' and user.role.RoleName != '协管员'):
			raise myError('对不起,您没有该权限!')
		book = Book()
		BookID = data['book']['book_id']
		existBook = Book()
		existBook = Book.objects.filter(BookID=BookID).first()
		if existBook:
			raise myError('该图书编号已存在')
		book.BookID = BookID
		book.BookNo = data['book']['book_no']
		book.BookName = data['book']['book_name']
		book.BookWriter = data['book']['book_writer']
		book.BookPublish = data['book']['book_publish']
		book.BookPrice = data['book']['book_price']
		book.BookState = data['book']['book_state']
		book.BookRNo = data['book']['book_rno']
		book.BookDate = noneIfEmptyString(data['book']['book_date'])
		if not noneIfEmptyString(data['book']['book_class']):
			ClassName=data['book']['book_class']
			bookclass = BookClasses.objects.filter(ClassName=ClassName).first()
			book.BookClass = bookclass
		if not noneIfEmptyString(data['book']['book_main']):
			book.BookMain = data['book']['book_main']
		if not noneIfEmptyString(data['book']['book_prim']):
			book.BookPrim = data['book']['book_prim']
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

def deleteBook(request):
	try:
		data = json.loads(request.body)
		token = Token()
		token = Token.objects.filter(token=data['token']).first()
		user = User()
		user = token.user
		if (user.role.RoleName != '管理员' and user.role.RoleName != '协管员'):
			raise myError('对不起,您没有该权限!')
		BookID = data['book']['book_id']
		book = Book()
		book = Book.objects.filter(BookID=BookID).first()
		borrowInfo = BorrowInfo()
		borrowInfo = BorrowInfo.objects.filter(book=book).first()
		if borrowInfo:
			raise myError('该书已被借出,不能删除!')
		lost = LostBook()
		lost = LostBook.objects.filter(book=book).first()
		if lost:
			raise myError('该书在遗失表中，不能删除!')
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

def updateBook(request):
	try:
		data = json.loads(request.body)
		token = Token()
		token = Token.objects.filter(token=data['token']).first()
		user = User()
		user = token.user
		if (user.role.RoleName != '管理员' and user.role.RoleName != '协管员'):
			raise myError('对不起,您没有该权限!')
		book = Book()
		book = Book.objects.filter(BookID=data['book']['book_id']).first()
		if not book:
			raise myError('该书不存在')
		if 'book_name' in data['book']:
			book.BookName = data['book']['book_name']
		if 'book_writer' in data['book']:
			book.BookWriter = data['book']['book_writer']
		if 'book_publish' in data['book']:
			book.BookPublish = data['book']['book_publish']
		if 'book_price' in data['book']:
			book.BookPrice = data['book']['book_price']
		if 'book_date' in data['book']:
			book.BookDate = data['book']['book_date']
		if 'book_state' in data['book']:
			book.BookState = bool(data['book']['book_state'])
		if 'book_rno' in data['book']:
			book.BookRNo = data['book']['book_rno']
		if 'book_no' in data['book']:
			book.BookNo = data['book']['book_no']
		if 'book_class' in data['book']:
			ClassName=data['book']['book_class']
			bookclass = BookClasses.objects.filter(ClassName=ClassName).first()
			book.BookClass = bookclass
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

def borrowBook(request):
	try:
		data = json.loads(request.body)
		token = Token()
		token = Token.objects.filter(token=data['token']).first()
		user = User()
		user = token.user
		if (user.role.RoleName != '管理员' and user.role.RoleName != '协管员'):
			raise myError('对不起,您没有该权限!')
		borrow = BorrowInfo()
		BookID = data['book']['book_id']
		ReaderID = data['user']['user_id']
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
		existBorrow = BorrowInfo.objects.filter(book=book).first()
		if existBorrow:
			raise myError('该书已被借出!')
		fine = FineInfo()
		fine = FineInfo.objects.filter(reader=user).first()
		if fine and not fine.PayState:
			raise myError('该用户有罚款未缴纳,不能借书!')
		if user.BorrowNumber > user.MaxBorrowNumber:
			raise myError('该用户借书本数已达可借本书上限值!')
		borrow.book = book
		borrow.reader = user
		borrow.BackTime = datetime.date.today() + datetime.timedelta(days=60)
		book.BookState = False
		user.BorrowNumber += 1
		user.TotalBorrow += 1
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

def returnBook(request):
	try:
		data = json.loads(request.body)
		token = Token()
		token = Token.objects.filter(token=data['token']).first()
		user = User()
		user = token.user
		if (user.role.RoleName != '管理员' and user.role.RoleName != '协管员'):
			raise myError('对不起,您没有该权限!')
		BookID = data['book']['book_id']
		book = Book()
		book = Book.objects.filter(BookID=BookID).first()
		if not book:
			raise myError('该图书编号不存在,请检查是否输入错误!')
		borrow = BorrowInfo()
		borrow = BorrowInfo.objects.filter(book=book).first()
		if not borrow:
			raise myError('不存在该借阅信息,请检查是否输入错误!')
		UserID = borrow.reader.UserID
		user = User()
		user = User.objects.filter(UserID=UserID).first()
		user.BorrowNumber -= 1
		book.BookState = True
		book.save()
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

def finePayment(request):
	try:
		data = json.loads(request.body)
		token = Token()
		token = Token.objects.filter(token=data['token']).first()
		user = User()
		user = token.user
		if (user.role.RoleName != '管理员' and user.role.RoleName != '协管员'):
			raise myError('对不起,您没有该权限!')
		UserID = data['user']['user_id']
		fineInfo = FineInfo()
		reader = User.objects.filter(UserID=UserID).first()
		fineInfo = FineInfo.objects.filter(reader=reader)
		for fine in fineInfo:
			fine.PayState = True
			fine.PayDate = datetime.date.today()
			fine.admin = user
			fine.save()
		user = User.objects.filter(UserID=UserID).first()
		user.Fine = 0
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

def lostFine(request):
	try:
		data = json.loads(request.body)
		token = Token()
		token = Token.objects.filter(token=data['token']).first()
		user = User()
		user = token.user
		if (user.role.RoleName != '管理员' and user.role.RoleName != '协管员'):
			raise myError('对不起,您没有该权限!')
		BookID = data['book']['book_id']
		ReaderID = data['user']['user_id']
		book = Book()
		book = Book.objects.filter(BookID=BookID).first()
		if not book:
			raise myError('该书不存在,请检查是否编号输入错误!')
		borrowInfo = BorrowInfo()
		borrowInfo = BorrowInfo.objects.filter(book=book).first()
		if not borrowInfo:
			raise myError('该书未被借出,请检查是否编号输入错误!')
		reader = User.objects.filter(UserID=ReaderID).first()
		lostBook = LostBook()
		UserID = borrowInfo.reader.UserID
		lostBook.book = book
		lostBook.reader = reader
		lostBook.PayMoney = book.BookPrice * 2
		lostBook.admin = user
		user = User.objects.filter(UserID=UserID).first()
		user.BorrowNumber -=1
		borrowInfo.delete()
		user.save()
		lostBook.save()
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

def deleteLostBook(request):
	try:
		data = json.loads(request.body)
		token = Token()
		token = Token.objects.filter(token=data['token']).first()
		user = User()
		user = token.user
		if (user.role.RoleName != '管理员'):
			raise myError('对不起,您没有该权限!')
		BookID = data['book']['book_id']
		book = Book()
		book = Book.objects.filter(BookID=BookID).first()
		strDate = data['date']['operate_date']
		OperateDate = datetime.datetime.strptime(strDate,'%Y-%m-%d')
		print OperateDate
		lostBook = LostBook()
		lostBook = LostBook.objects.filter(book=book, OperateDate=OperateDate).first()
		lostBook.delete()
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

def allBookClasses(request):
	try:
		data = json.loads(request.body)
		token = Token()
		token = Token.objects.filter(token=data['token']).first()
		user = User()
		user = token.user
		if (user.role.RoleName != '管理员' and user.role.RoleName != '协管员'):
			raise myError('对不起,您没有该权限!')
		classList = []
		all_bookClasses = BookClasses.objects.all()
		for bookClass in all_bookClasses:
			classList.append({
				'book_class_name': bookClass.ClassName,
				'book_class_id': bookClass.id
				})
		result = {
			'successful': True,
			'data': classList,
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

def addBookClasses(request):
	try:
		data = json.loads(request.body)
		token = Token()
		token = Token.objects.filter(token=data['token']).first()
		user = User()
		user = token.user
		if (user.role.RoleName != '管理员' and user.role.RoleName != '协管员'):
			raise myError('对不起,您没有该权限!')
		ClassName = data['book']['book_class']
		existClass = BookClasses.objects.filter(ClassName=ClassName).first()
		if existClass:
			raise myError('该图书类别已存在!')
		bookClass = BookClasses()
		bookClass.ClassName = ClassName
		bookClass.save()
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

def deleteBookClass(request):
	try:
		data = json.loads(request.body)
		token = Token()
		token = Token.objects.filter(token=data['token']).first()
		user = User()
		user = token.user
		if (user.role.RoleName != '管理员' and user.role.RoleName != '协管员'):
			raise myError('对不起,您没有该权限!')
		ClassName = data['book']['book_class']
		bookClass = BookClasses()
		bookClass = BookClasses.objects.filter(ClassName=ClassName).first()
		if not bookClass:
			raise myError('该图书类别不存在')
		books = Book()
		books = Book.objects.filter(BookClass=bookClass)
		for book in books:
			book.BookClass = None
			books.save()
		bookClass.delete()
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

def updateBookClass(request):
	try:
		data = json.loads(request)
		token = Token()
		token = Token.objects.filter(token=data['token']).first()
		user = User()
		user = token.user
		if (user.role.RoleName != '管理员' and user.role.RoleName != '协管员'):
			raise myError('对不起,您没有该权限!')
		classID = date['class']['class_id']
		ClassName = data['class']['class_name']
		existClass = BookClasses()
		existClass = BookClasses.objects.filter(ClassName=ClassName).first()
		if existClass:
			raise myError('该类别名已存在!')
		bookClass = BookClasses()
		bookClass = BookClasses.objects.filter(id=class_id).first()
		bookClass.ClassName = ClassName
		bookClass.save()
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