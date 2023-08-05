# -*- coding: utf-8 -*-
from settings.models import Globals, addGlobalContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render


def home(request):
    config = Globals()
    context = {'config': config}
    if request.method == "POST":
        settings = request.POST
        org_long_name = settings.get("org_long_name", None)
        org_short_name = settings.get("org_short_name", None)
        org_motto = settings.get("org_motto", None)
        late_fees_price = settings.get("late_fees_price", None)
        config = Globals()
        if org_long_name is not None:
            config.add("alms", "org_long_name", org_long_name)
        if org_short_name is not None:
            config.add("alms", "org_short_name", org_short_name)
        if org_motto is not None:
            config.add("alms", "org_motto", org_motto)
        if late_fees_price is not None:
            config.add("misc", "late_fees_price", late_fees_price)

        return HttpResponseRedirect(reverse("settingsHome"))

    return render(request,
                  "settings/home.html",
                  addGlobalContext(context))
