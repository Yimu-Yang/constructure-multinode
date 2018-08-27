# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

import datetime

class Companys(models.Model):
    company_name = models.TextField(max_length=100)

class Projects(models.Model):
	project_name = models.TextField(max_length=100)

class Users(models.Model):
	user_name = models.TextField(max_length=30)
	password = models.CharField(max_length=100)
	cell = models.TextField(max_length=20)
	position = models.TextField(max_length=10)
	card_id = models.TextField(max_length=19)
	thumbnail_id = models.TextField(max_length=32)

class Experiences(models.Model):
	user = models.ForeignKey(Users, on_delete=models.CASCADE,
		db_index=True)
	company = models.ForeignKey(Companys, on_delete=models.CASCADE,
		db_index=True)
	project = models.ForeignKey(Projects, on_delete=models.CASCADE,
		db_index=True)
	todo = models.IntegerField(default=5)
	start = models.DateField(default=datetime.date.today)
	duration = models.IntegerField(default=1)
	job = models.TextField(max_length=10)

class ToVerify(models.Model):
	user = models.ForeignKey(Users, on_delete=models.CASCADE,
		db_index=True)
	experience = models.ForeignKey(Experiences, on_delete=models.CASCADE,
		db_index=True)
