# -*- coding:utf-8 -*-
from django.core.mail import EmailMultiAlternatives
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from urllib import urlencode

def send_verificationEmail(to_email):
	try :
		s = Serializer('SECRET_KEY', 3600)
		code = s.dumps({'confirm': to_email})
		from_email = 'ch940068139@126.com'
		subject = '图书管理系统'
		to_email = to_email
		value = {'confirm': code}
		data = urlencode(value)
		url = 'localhost:8000/myapp/user/confirm' + '?' + data
		text_content = "这是一封很重要的邮件!"
		html_content = u'<p>尊敬的用户，您的激活链接为:<a href="http://%s">%s</a> \
			 ,请注意查收保管,验证码有效时间为1小时, 请在有效期内点击链接验证您的邮箱。</p>' %(url, url)
		msg = EmailMultiAlternatives(subject,text_content,from_email,[to_email])
		msg.attach_alternative(html_content, 'text/html')
		msg.send()
	except Exception, e:
		print e.args