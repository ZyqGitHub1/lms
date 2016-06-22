from django.shortcuts import render
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

def updateUserInfo(request):
	try:
		data = json.loads(request.body)
		token = Token()
		token = Token.objects.filter(token=data['token'])
		user = User()
		user = token.user
		if user.RoleName != '管理员' &&
			user.RoleName != '协管员':
			raise myError('对不起,您没有该权限!')
		