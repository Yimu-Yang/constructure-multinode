# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
import traceback

from . import models

from .utils import prefixes
from .utils import logger

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
    obj = {}
    obj["status"] = 0
    obj["result"] = {}
    try:
        if request.method == "GET":
            prefix = request.GET.get('prefix')
            string = prefixes.search_company(prefix)
            return HttpResponse("{\"status\": 1, \"result\": %s, \"message\":\"\"" % string)
        obj["message"] = "unknown method"
        return HttpResponse(json.dumps(obj))
    except Exception as e:
        logging.log(traceback.format_exc())
        obj["message"] = e.message
        return HttpResponse(json.dumps(obj))

def search_user(request):
    obj = {}
    obj["status"] = 0
    obj["result"] = {}
    try:
        if request.method == "GET":
            prefix = request.GET.get('prefix')
            string = prefixes.search_people(prefix)
            return HttpResponse("{\"status\": 1, \"result\": %s, \"message\":\"\"" % string)
        obj["message"] = "unknown method"
        return HttpResponse(json.dumps(obj))
    except Exception as e:
        logging.log(traceback.format_exc())
        obj["message"] = e.message
        return HttpResponse(json.dumps(obj))

def search_worker(request):
    return HttpResponse("Search Worker\n")

def search_connection(request):
    return HttpResponse("Search Connection\n")