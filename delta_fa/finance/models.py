from django.db import models
from dashboard.models import User,CourseInfo
import datetime

# Create your models here.


class Account(models.Model):
    account_number = models.CharField(max_length=10,default = "")
    user = models.OneToOneField(User,on_delete = models.CASCADE,related_name='account')
    balance = models.FloatField(default = 0)

    def __str__(self):
        return self.user.__str__() + f", {self.account_number}"

class Invoice(models.Model):
    account = models.ForeignKey(Account,on_delete = models.CASCADE,null = False,blank = False,related_name = 'invoices')
    course = models.ForeignKey(CourseInfo,on_delete = models.PROTECT,null = False,blank = False,related_name = 'invoices')
    serial = models.CharField(max_length = 128,null = False,blank = False)
    amount = models.FloatField(null = False,blank = False)
    init_date = models.DateTimeField(auto_now_add=True)
    payment_due = models.DateTimeField(null = False,blank = False)
    discount = models.IntegerField()


    def checkout(self,with_discount):
        if with_discount:
            self.amount *=(100-self.discount)/100
        self.account.balance += self.amount
        receipt = Receipt(account = self.account,course = self.course,serial = "paid_"+self.serial,amount = self.amount)
        receipt.save()
        self.account.save()

    def __str__(self):
        return f"{self.serial}"

class Receipt (models.Model):
    account = models.ForeignKey(Account,on_delete = models.CASCADE,null = False,blank = False,related_name = 'receipt')
    course = models.ForeignKey(CourseInfo,on_delete = models.PROTECT,null = False,blank = False,related_name = 'receipt')
    serial = models.CharField(max_length = 128,null = False,blank = False)
    amount = models.FloatField(null = False,blank = False)
    checkout_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.serial}"
