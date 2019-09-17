from django.contrib.sites import requests
from django.http import HttpResponse
from django.shortcuts import render


def cancel_payment(request):
    print(request)
    print("cancel_payment")
    return render(request, "main/cancelpayment.html")


def process_payment(request):
    # print(request)
    print("process payment")
    # tx = request.GET.get("tx")
    print("---------------------------")
    # print(tx)
    print("---------------------------")
    return render(request, "main/donepayment.html")



