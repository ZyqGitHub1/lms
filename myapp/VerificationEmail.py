# -*- coding:utf-8 -*-
from django.core.mail import send_mail

def send_verificationEmail(to_email, code):
		from_email = 'chenghao940068139@gmail.com'
		subject = '图书管理系统'
		to_email = to_email
		message = '尊敬的用户，您的验证码为' + code + \
			 ',请注意查收保管,验证码有效时间为1小时, 请在有效期内在相应网页验证您的邮箱。'
		send_mail(subject, message, from_email, [to_email])