# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You're at the login index.")

def login(request):
	return HttpResponse("Login")

def logout(request):
	return HttpResponse("Logout")

def reset_password(request):
	return HttpResponse("Reset Password")