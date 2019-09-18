import urllib

from django.contrib.sites import requests
from django.http import HttpResponse
from django.shortcuts import render

from annoncestracker import settings
from main.signals import paypal


def cancel_payment(request):
    print(request)
    print("cancel_payment")
    return render(request, "main/cancelpayment.html")


def process_payment(request):
    # print(request)
    print("process payment")
    tx = request.GET.get("tx")
    print("---------------------------")
    # print(tx)
    print("---------------------------")
    result = paypal.Verify(tx)
    if result.success():  # valid
        print("yeeeeeeeeeeeeeeeeeeep")
    return render(request, "main/donepayment.html")



