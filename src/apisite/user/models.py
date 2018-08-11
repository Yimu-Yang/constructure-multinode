# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Companys(models.Model):
    company_name = models.TextField(max_length=100)

class Users(models.Model):
	user_name = models.TextField(max_length=30)
	password = models.CharField(max_length=100)
	status = models.IntegerField(default=1)
	company = models.ForeignKey(Companys, on_delete=models.CASCADE,
		db_index=True)

class ToVerify(models.Model):
	verifier = models.ForeignKey(Users, on_delete=models.CASCADE,
		related_name='toverify_verifier', db_index=True)
	verifiee = models.ForeignKey(Users, on_delete=models.CASCADE,
		related_name='toverify_verifiee', db_index=True)

class Cooperation(models.Model):
	contractor = models.ForeignKey(Users, on_delete=models.CASCADE,
		related_name='cooperation_contractor')
	contractee = models.ForeignKey(Users, on_delete=models.CASCADE,
		related_name='cooperation_contractee')
	contractor_company = models.ForeignKey(Companys, on_delete=models.CASCADE,
		related_name='cooperation_contractor_company')
	contractee_company = models.ForeignKey(Companys, on_delete=models.CASCADE,
		related_name='cooperation_contractee_company')
	duration = models.IntegerField(default=30)
	project = models.TextField(max_length=500)

class CompaniedUsers(models.Model):
	user_company = models.TextField(max_length=140)
	user_table_id = models.IntegerField(default=0)