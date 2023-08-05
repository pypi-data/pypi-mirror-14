# -*- coding: utf-8 -*-
from django.shortcuts import render

from settings.models import addGlobalContext
# Create your views here.

def home(request):
    context = addGlobalContext({})
    return render(request, "booktool/home.html", context=context)
