from django.shortcuts import render


def cancel_payment(request):
    print(request)
    print("i'm here")
    return render(request, "main/cancelpayment.html")


def process_payment(request):
    print(request)
    print("i'm here")
    return render(request, "main/donepayment.html")

