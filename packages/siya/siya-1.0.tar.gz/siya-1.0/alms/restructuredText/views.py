# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.utils.encoding import smart_str
from django.core.urlresolvers import reverse

from settings.models import addGlobalContext
# Create your views here.

from .models import RestructuredText


def writeHomeBody(request):
    homeBody = RestructuredText.objects.get(name="homeBody")
    context = {
        "body": homeBody.get_rst()
        }
    if request.method == "POST":
        rst = request.POST.get("rst", None)
        if rst is not None:
            homeBody.set_rst(smart_str(rst))
            homeBody.save()
            return HttpResponseRedirect(reverse("writeHomeBody"))
    return render(request,
                  "restructuredText/editHomePage.html",
                  context=addGlobalContext(context))
