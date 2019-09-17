from django.shortcuts import render


def cancel_payment(request):

    return render(request, "main/cancelpayment.html")


def process_payment(request):

    return render(request, "main/donepayment.html")

