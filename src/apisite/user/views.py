# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse

import traceback
import json

from . import models

from .utils import prefixes
from .utils import logger
from .utils import authenticate

NEED_LOGIN_STATUS = 2
NEED_LOGIN_MESSAGE = "Needs Login"

# TODO: Token timeout, and authentication exception

def login(request):
    obj = {}
    obj["status"] = 0
    obj["result"] = {}
    obj["message"] = ""
    try:
        if request.method == "POST":
            body = json.loads(request.body)
            user_id = body["id"]
            password = body["password"]
            user = models.Users.objects.get(pk=user_id)
            if user.password == password:
                obj["result"] = {"status": user.status,
                                 "token": authenticate.generate_authentication_token(user_id)}
                obj["status"] = 1
                return HttpResponse(json.dumps(obj))
        obj["message"] = "unknown method"
        return HttpResponse(json.dumps(obj))
    except Exception as e:
        logger.log(traceback.format_exc())
        obj["message"] = e.message
        return HttpResponse(json.dumps(obj))

def handle_uploaded_file(f):
    # FIXME
    with open('/tmp/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def upload_picture(request):
    if request.method == "POST":
        print(request.FILES)
        print(type(request.FILES['picture']))
        handle_uploaded_file(request.FILES['picture'])
        return HttpResponse("upload OK\n")
    return HttpResponse("uploadfailed \n")


def logout(request):
    return HttpResponse("Logout \n")

def reset_password(request):
    return HttpResponse("Reset Password \n")

def register(request):
    obj = {}
    obj["status"] = 0
    obj["result"] = {}
    obj["message"] = ""
    try:
        if request.method == "POST":
            body = json.loads(request.body)
            user = models.Users(user_name=body['name'],
                                password=body['password'],
                                company=models.Companys.objects.get(pk=int(body['companyId'])))
            user.save()
            user_id = user.id
            obj["result"] = {"token": authenticate.generate_authentication_token(user_id),
                             "userId": user_id}
            obj["status"] = 1
            return HttpResponse(json.dumps(obj))
        obj["message"] = "unknown method"
        return HttpResponse(json.dumps(obj))
    except Exception as e:
        logger.log(traceback.format_exc())
        obj["message"] = e.message
        return HttpResponse(json.dumps(obj))

def request_verify(request):
    obj = {}
    obj["status"] = 0
    obj["result"] = {}
    obj["message"] = ""
    try:
        if request.method == "POST":
            body = json.loads(request.body)
            user_id = authenticate.verify_authentication_token(request.META.get("HTTP_TOKEN"))
            # Needs login
            if not user_id:
                obj["status"] = NEED_LOGIN_STATUS
                obj["message"] = NEED_LOGIN_MESSAGE
                return HttpResponse(json.dumps(obj))

            verifiee = models.Users.objects.get(pk=user_id)
            for x in body["requestVerifyUser"]:
                # If already exists, Pass
                if models.ToVerify.objects.filter(verifier=x, verifiee=user_id).count():
                    continue
                # Else add to ToVerify Table
                to_verify = models.ToVerify(verifier=models.Users.objects.get(pk=int(x)),
                                            verifiee=verifiee)
                to_verify.save()
            # Check total number of requested verifier
            if models.ToVerify.objects.filter(verifiee=user_id).count() < 5:
                # If not enough: fail and warn user
                obj["message"] = "Needs more than 5 verifier"
                return HttpResponse(json.dumps(obj))
            # At least 5 verifier, success
            # Change user status to pending verification instead of "DEFAULT"
            verifiee.status = USER_PENDING_VERIFICATION # MEANS pending verification
            verifiee.save()
            obj["status"] = 1
            return HttpResponse(json.dumps(obj))
        obj["message"] = "unknown method"
        return HttpResponse(json.dumps(obj))
    except Exception as e:
        logger.log(traceback.format_exc())
        obj["message"] = e.message
        return HttpResponse(json.dumps(obj))

def get_verify_status(request):
    obj = {}
    obj["status"] = 0
    obj["result"] = {}
    obj["message"] = ""
    try:
        if request.method == "GET":
            user_id = authenticate.verify_authentication_token(request.META.get("HTTP_TOKEN"))
            # Needs login
            if not user_id:
                obj["status"] = NEED_LOGIN_STATUS
                obj["message"] = NEED_LOGIN_MESSAGE
                return HttpResponse(json.dumps(obj))

            result = []
            for x in models.ToVerify.objects.filter(verifier=user_id):
                result.append({"name": x.verifiee.user_name, "id": x.verifiee.id})
            obj["result"] = result
            obj["status"] = 1
            return HttpResponse(json.dumps(obj))
        obj["message"] = "unknown method"
        return HttpResponse(json.dumps(obj))
    except Exception as e:
        logger.log(traceback.format_exc())
        obj["message"] = e.message
        return HttpResponse(json.dumps(obj))

def verify_user(request):
    obj = {}
    obj["status"] = 0
    obj["result"] = {}
    obj["message"] = ""
    try:
        if request.method == "POST":
            body = json.loads(request.body)
            user_id = authenticate.verify_authentication_token(request.META.get("HTTP_TOKEN"))
            # Needs login
            if not user_id:
                obj["status"] = NEED_LOGIN_STATUS
                obj["message"] = NEED_LOGIN_MESSAGE
                return HttpResponse(json.dumps(obj))

            verifiee_id = body["userId"]
            # Change verification status to 1
            to_verify = models.ToVerify.objects.get(verifiee=verifiee_id, verifier=user_id)
            to_verify.verified = 1
            to_verify.save()
            # If more than 5 verifier has verified verifiee
            if models.ToVerify.objects.filter(verifiee=verifiee_id, verified=1).count() >= 5:
                verifiee = models.Users.objects.get(pk=verifiee_id)
                verifiee.status = USER_NORMAL
                verifiee.save()
                # Cleanup ToVerify table
                models.ToVerify.objects.filter(verifiee=verifiee_id).delete()
            obj["status"] = 1
            return HttpResponse(json.dumps(obj))
        obj["message"] = "unknown method"
        return HttpResponse(json.dumps(obj))
    except Exception as e:
        logger.log(traceback.format_exc())
        obj["message"] = e.message
        return HttpResponse(json.dumps(obj))


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
        logger.log(traceback.format_exc())
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
        logger.log(traceback.format_exc())
        obj["message"] = e.message
        return HttpResponse(json.dumps(obj))

def search_worker(request):
    obj = {}
    obj["status"] = 0
    obj["result"] = {}
    try:
        if request.method == "GET":
            company_id = request.GET.get('companyId')
            user_id = authenticate.verify_authentication_token(request.META.get("HTTP_TOKEN"))
            # Needs login
            if not user_id:
                obj["status"] = NEED_LOGIN_STATUS
                obj["message"] = NEED_LOGIN_MESSAGE
                return HttpResponse(json.dumps(obj))

            result = []
            for x in models.Users.objects.filter(company_id=company_id):
                result.append({"name": x.user_name, "id": x.id})
            obj["result"] = result
            obj["status"] = 1
            return HttpResponse(json.dumps(obj))
        obj["message"] = "unknown method"
        return HttpResponse(json.dumps(obj))
    except Exception as e:
        logger.log(traceback.format_exc())
        obj["message"] = e.message
        return HttpResponse(json.dumps(obj))

def cooperation(request):
    obj = {}
    obj["status"] = 0
    obj["result"] = {}
    try:
        if request.method == "GET":
            target_id = request.GET.get('id')
            user_id = authenticate.verify_authentication_token(request.META.get("HTTP_TOKEN"))
            # Needs login
            if not user_id:
                obj["status"] = NEED_LOGIN_STATUS
                obj["message"] = NEED_LOGIN_MESSAGE
                return HttpResponse(json.dumps(obj))

            obj["result"] = _get_cooperation(user_id, target_id)
            obj["status"] = 1
            return HttpResponse(json.dumps(obj))
        obj["message"] = "unknown method"
        return HttpResponse(json.dumps(obj))
    except Exception as e:
        logger.log(traceback.format_exc())
        obj["message"] = e.message
        return HttpResponse(json.dumps(obj))

def _get_cooperation(user_id, target_id):
    partyA = models.Users.objects.get(pk=user_id)
    partyB = models.Users.objects.get(pk=target_id)
    history = []
    for x in models.Experiences.objects.filter(project__experiences__user_id=user_id,
                                              todo=0, project__experiences__todo=0,
                                              user_id=target_id):
        history.append({"job": x.job,
                        "duration": x.duration,
                        "content": x.project.project_name})
    for x in models.Experiences.objects.filter(company__experiences__user_id=user_id,
                                              todo=0, company__experiences__todo=0,
                                              user_id=target_id):
        history.append({"job": x.job,
                        "duration": x.duration,
                        "content": x.company.company_name})
    return {"partyA": {"name": partyA.user_name, "job": partyA.position},
            "partyB": {"name": partyB.user_name, "job": partyB.position},
            "history": history}

def search_connection(request):
    obj = {}
    obj["status"] = 0
    obj["result"] = {}
    try:
        if request.method == "GET":
            target_id = request.GET.get('id')
            user_id = authenticate.verify_authentication_token(request.META.get("HTTP_TOKEN"))
            # Needs login
            if not user_id:
                obj["status"] = NEED_LOGIN_STATUS
                obj["message"] = NEED_LOGIN_MESSAGE
                return HttpResponse(json.dumps(obj))

            obj["result"] = _get_connection(user_id, target_id)
            obj["status"] = 1
            return HttpResponse(json.dumps(obj))
        obj["message"] = "unknown method"
        return HttpResponse(json.dumps(obj))
    except Exception as e:
        logger.log(traceback.format_exc())
        obj["message"] = e.message
        return HttpResponse(json.dumps(obj))

def _get_neighbors_company(id):
    res = []
    for x in models.Experiences.objects.filter(company__experiences__user_id=id,
                                        todo=0, company__experiences__todo=0):
        res.append((x.user.user_name, x.user.id, duration))
    return res

def _get_neighbors_cooperator(id):
    res = []
    for x in models.Experiences.objects.filter(project__experiences__user_id=id,
                                        todo=0, project__experiences__todo=0):
        res.append((x.user.user_name, x.user.id, duration))
    return res


def _get_neighbors(id):
    visited = set()
    visited.add(id)
    for x in _get_neighbors_company(id):
        if x[1] in visited:
            continue
        visited.add(x[1])
        yield x
    for x in _get_neighbors_project(id):
        if x[1] in visited:
            continue
        visited.add(x[1])
        yield x

def _to_readable(days):
    if days < 365:
        return "%d月" % (days/30 + 1)
    return "%d年" % (days/365 + 1)

def _process_result(connection_result):
    res = []
    for x in connection_result[1:]:
        res.append({"name": x[0], "id": x[1], "year": _to_readable(x[2])})
    return res

def _get_connection(user_id, target_id):
    # DFS
    result = []

    start_user = models.Users.objects.get(pk=user_id)
    curr = [(start_user.user_name, user_id, 0)]
    visited = set([user_id])

    def dfs(curr, visited):
        for x in _get_neighbors(curr[-1][1]):
            if x[1] == target_id:
                curr.append(x)
                # Process Result
                result.append(_process_result(curr))
                curr.pop()
            if x in visited:
                continue
            visited.add(x)
            curr.append(x)
            dfs(curr, visited)
            curr.pop()

    dfs(curr, visited)

    list.sort(result, key=len)

    return result











