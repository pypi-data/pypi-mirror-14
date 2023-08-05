# -*- coding: utf-8 -*-
from django.shortcuts import render

# Create your views here.

from settings.models import addGlobalContext
from .models import GenericField, GenericFieldLink
from head.models import Book
from django.contrib.auth.decorators import login_required, permission_required

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


@login_required(login_url="/login/")
@permission_required(
        ("head.delete_book", "head.change_book"), login_url="/login/")
def home(request):
    miscFields = GenericField.objects.order_by('-last_modified')
    return render(request, 'miscFields/home.html', addGlobalContext(
                                                {
                                                    'miscfields': miscFields
                                                    }
                                                    )
                  )


@login_required(login_url="/login/")
@permission_required(
        ("head.delete_book", "head.change_book"), login_url="/login/")
def addNewField(request):
    status = 0   # start with status "success" ;)
    # status values:
    # 0 - success
    # 1 - invalid accession number
    # 2 - invalid field name

    print request.method
    if request.method.upper() == "POST":
        key = request.POST.get("key", None)
        print key
        if key not in [None, ""]:
            gen_field = GenericField.objects.create(key=key)
            accNo = request.POST.get("accNo", None)
            if key not in [None, ""]:
                if accNo is not None:
                    book = Book.objects.get(accession_number=accNo)
                    gen_field_link = GenericFieldLink.objects.create(
                            value="",
                            book=book)
                    gen_field_link.save()
                    gen_field.value.add(gen_field_link)
                    gen_field.save()
            else:
                status = 1
        else:
            status = 2

        if status == 0:
            if accNo is not None:
                return HttpResponseRedirect(reverse("book", kwargs={"accNo": accNo}))
        else:
            return HttpResponseRedirect(reverse("home"))
    return HttpResponseRedirect(reverse("miscFieldsHome"))


@login_required(login_url="/login/")
@permission_required(
        ("head.delete_book", "head.change_book"), login_url="/login/")
def delete_field(request, field_id):
    state = 1
    field = GenericField.objects.get(id=field_id)
    if request.method.upper() == "POST":
        delete = request.POST.get("delete", None)
        if delete is None:
            pass
        else:
            field.delete()
            state = 0
            return HttpResponseRedirect(reverse("miscFieldsHome"))

    return render(request,
                  "miscFields/delete_field.html",
                  addGlobalContext(
                      {
                          "state": state,
                          "field": field
                      }))


@login_required(login_url="/login/")
@permission_required(
        ("head.delete_book", "head.change_book"), login_url="/login/")
def edit_field(request, field_id):
    state = 1
    field = GenericField.objects.get(id=field_id)
    if request.method.upper() == "POST":
        name = request.POST.get("field_name", None)
        if name is None:
            pass
        else:
            field.key = name
            field.save()
            state = 0
            return HttpResponseRedirect(reverse("miscFieldsHome"))

    return render(request,
                  "miscFields/edit_field.html",
                  addGlobalContext(
                      {
                          "state": state,
                          "field_id": field_id,
                          "field": field
                      }))
