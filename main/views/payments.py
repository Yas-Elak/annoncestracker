from django.contrib.sites import requests
from django.http import HttpResponse
from django.shortcuts import render


def cancel_payment(request):
    print(request)
    print("i'm here")
    return render(request, "main/cancelpayment.html")


def process_payment(request):
    print(request)
    print("i'm here")
    return render(request, "main/donepayment.html")


def paypal_ipn(request):
    if request.method == 'POST':
        print("ipppppnnnnnnnnn")
    return HttpResponse('<h1>Page was found</h1>')

