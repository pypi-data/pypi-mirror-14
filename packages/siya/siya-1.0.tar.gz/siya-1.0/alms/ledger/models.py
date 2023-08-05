# -*- coding: utf-8 -*-
'''

 _____ _             ____      _              ___   __ 
|_   _| |__   ___   / ___|_ __(_) ___  ___   / _ \ / _|
  | | | '_ \ / _ \ | |   | '__| |/ _ \/ __| | | | | |_ 
  | | | | | |  __/ | |___| |  | |  __/\__ \ | |_| |  _|
  |_| |_| |_|\___|  \____|_|  |_|\___||___/  \___/|_|  
                                                       
  ____ _     _ _     _                  _   _            _     __  __      
 / ___| |__ (_) | __| |_ __ ___ _ __   | | | |_   _ _ __| |_  |  \/  | ___ 
| |   | '_ \| | |/ _` | '__/ _ \ '_ \  | |_| | | | | '__| __| | |\/| |/ _ \
| |___| | | | | | (_| | | |  __/ | | | |  _  | |_| | |  | |_  | |  | |  __/
 \____|_| |_|_|_|\__,_|_|  \___|_| |_| |_| |_|\__,_|_|   \__| |_|  |_|\___|
                                                                           

If you can dream-and not make dreams your master;   
    If you can think-and not make thoughts your aim;   
If you can meet with Triumph and Disaster
    And treat those two impostors just the same;   
If you can bear to hear the truth you've spoken
    Twisted by knaves to make a trap for fools,
Or watch the things you gave your life to, broken,
    And stoop and build 'em up with worn-out tools: 
'''


from django.db import models

# Create your models here.

def getCurrency(value):
    return "Rs.{:,}".format(value)



class DrCr(models.Model):
    '''
    Class for either Debit
    or credit
    '''
    particulars = models.CharField(max_length=500)
    amount = models.FloatField()

    def getAmount(self):
        return self.amount

    def getParticulars(self):
        if self.particulars != "None" or self.particulars == None:
            return self.particulars
        else:
            return "N/A"


class Debit(DrCr):
    def __str__(self):
        return "Debit : {}".format(self.getParticulars)


class Credit(DrCr):
    def __str__(self):
        return "Credit : {}".format(self.getParticulars)


class OneDaysEntry(models.Model):
    '''
    All The Entries made in he journal
    for that one day
    '''
    date = models.DateField(unique=True)
    debits = models.ManyToManyField(Debit,default=None)
    credits = models.ManyToManyField(Credit, default=None)

    def getDate(self):
        return self.date

    def getTotalCredit(self):
        return sum([_.amount for _ in self.credits.all()])

    def getTotalDebit(self):
        return sum([_.amount for _ in self.debits.all()])

    def getTotalCreditCur(self):
        return getCurrency(self.getTotalCredit())

    def getTotalDebitCur(self):
        return getCurrency(self.getTotalDebit())

    def totalBalanceMatchBool(self):
        total_debit = self.getTotalDebit()
        total_credit = self.getTotalCredit()
        return total_debit == total_credit

    def getDifferenceInBalance(self):
        balance = self.getTotalDebit() - self.getTotalCredit()
        if balance >= 0:
            sign = "+"
        else:
            sign = "-"
        return "{0}{1}".format(sign, balance)
    def __str__(self):
        return str(self.date)
