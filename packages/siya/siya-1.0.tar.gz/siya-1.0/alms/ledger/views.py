# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from settings.models import Globals, addGlobalContext
from ledger.models import OneDaysEntry, Credit, Debit

import datetime
# Create your views here.




def journalHomeArgs(request,
        addCreditSuccess=None,
        addDebitSuccess=None,
        particularsNotFound=None,
        debitNotFound=None,
        creditNotFound=None,
        debitNotInt=None,
        creditNotInt=None):
    '''
    journalHome with extra arguments
    '''
    context = {
            'globals': Globals,
            'date': datetime.date.today(),
            'date_add': datetime.date.today().isoformat(),
            'dayEntries': OneDaysEntry.objects.order_by("-date"),
            }

    context.update(
            [
                ["creditSuccess",addCreditSuccess],
                ["debitSuccess",addDebitSuccess],
                ['particularsNotFound',particularsNotFound],
                ['debitNotFound', debitNotFound],
                ['creditNotFound', creditNotFound],
                ['debitNotInt', debitNotInt],
                ['creditNotInt', creditNotInt]
                ])

    return render(request,'ledger/journalHome.html',context)


def journalHome(request):
    return journalHomeArgs(request)


def addDebit(request):
    id = request.POST.get("id",None)
    particular = request.POST.get("particular",None)
    amount = request.POST.get("debitAmount",None)
    if id in [None]:
        return journalHomeArgs(request,addCreditSuccess=False)
    elif particular in [None, ""]:
        return journalHomeArgs(request, particularsNotFound=True)
    elif amount in  [None, ""]:
        return journalHomeArgs(request, debitNotFound=True)
    elif str(amount).isdigit() is False:
        return journalHomeArgs(request, debitNotInt=True)
    else:
        oneDayEntry = OneDaysEntry.objects.get(id=id)
        debit = Debit.objects.create(
                particulars=particular,
                amount=amount
                )
        oneDayEntry.debits.add(debit)
        oneDayEntry.save()
        return HttpResponseRedirect(reverse("journalHome"))


def addCredit(request):
    id = request.POST.get("id",None)
    particular = request.POST.get("particular",None)
    amount = request.POST.get("creditAmount",None)
    if id == None or id == "":
        return journalHomeArgs(request,addCreditSuccess=False)
    elif particular in [None, ""]:
        return journalHomeArgs(request, particularsNotFound=True)
    elif amount in [None,""]:
        return journalHomeArgs(request, creditNotFound=True)
    elif str(amount).isdigit() is False:
        return journalHomeArgs(request, creditNotInt=True)
    else:
        oneDayEntry = OneDaysEntry.objects.get(id=id)
        credit = Credit.objects.create(
                particulars=particular,
                amount=amount
                )
        oneDayEntry.credits.add(credit)
        oneDayEntry.save()
        return HttpResponseRedirect(reverse("journalHome"))

def addOneDaysEntry(request):
    date_val = request.POST.get("date",None)
    if date_val == None:
        date = datetime.date.today()
    else:
        date_arr = date_val.split("-")
        date = datetime.date(int(date_arr[0]),int(date_arr[1]),int(date_arr[2]))
    OneDaysEntry.objects.create(date=date)
    return HttpResponseRedirect(reverse("journalHome"))



def showJournal(request,year,month):
    year = int(year)
    month = int(month)
    month = min(month,12)  #the value of month cannot be greater than 12
    date = datetime.date(year,month,1)
    date_str= date.strftime("%B of %Y")

    context = addGlobalContext()

    context.update({
            "day": date
        })


    return render(request, "ledger/journalDay.html",context)
