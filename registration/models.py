# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User

# Create your models here.

class Registration(models.Model):
    user = models.ForeignKey(User, default=1)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    registration_date = models.DateField('registration date')
    registration_time = models.TimeField('registration time')

    def __str__(self):
        return self.name + ' ' +self.surname

class regform(ModelForm):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    registration_date = models.DateField('registration date')
    registration_time = models.TimeField('registration time')

    class Meta:
        model = Registration
        fields = '__all__'