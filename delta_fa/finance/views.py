from django.shortcuts import render
# Create your views here.
from .models import *

def show_invoice(request):
    try:
        invoice = Account.objects.get(user = request.user).invoices.last()
    except Exception as e:
        invoice = 0
    data = {
        'invoice':invoice
    }
    print(invoice.init_date.year)
    return render(request,'html/dashboard/student/invoice.html',data)

def tranaction_history(request):
    try:
        receipt = Receipt.objects.filter(account = request.user.account)
    except Exception as e:
        receipt = 0
    data = {
        'receipt':receipt
    }
    return render(request,'html/dashboard/student/receipt.html',data)
