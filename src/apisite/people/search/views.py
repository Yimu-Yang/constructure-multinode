# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse

# Create your views here.
def prefix(request):
	return HttpResponse("Prefix")

def cooperators(request):
	return HttpResponse("Cooperators")

def cooperation(request):
	return HttpResponse("Cooperation")