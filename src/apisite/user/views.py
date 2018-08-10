# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse

from . import model

def login(request):
	return HttpResponse("Login \n")

def logout(request):
	return HttpResponse("Logout \n")

def reset_password(request):
	return HttpResponse("Reset Password \n")

def register(request):
	return HttpResponse("Register\n")

def request_verify(request):
	return HttpResponse("Request Verify\n")

def get_verify_status(request):
	return HttpResponse("Get Verify Status\n")

def verify_user(request):
	return HttpResponse("Verify User\n")

def search_company(request):
	return HttpResponse("Search Company\n")

def search_user(request):
	return HttpResponse("Search User\n")

def search_worker(request):
	return HttpResponse("Search Worker\n")

def search_connection(request):
	return HttpResponse("Search Connection\n")