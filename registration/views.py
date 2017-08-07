# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, render_to_response
from django.utils import timezone
from .models import Registration,regform
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def index(request):
    list_of_registrations = Registration.objects.all()
    #list_of_registrations = Registration.objects.filter(user=request.user) - jei reikia butent to userio
    return render(request, 'registration/index.html', {'list_of_registrations':list_of_registrations})

def reg_form(request):
    if request.method == 'POST':
        registration = regform(request.POST)
        if registration.is_valid():
            registration.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            messages.error(request, "Error")
    return render(request, 'registration/save.html', {'registration': regform(request.POST)},)
