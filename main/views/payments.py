from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


def cancel_payment(request):
    print(request)
    print("cancel_payment")
    return render(request, "main/cancelpayment.html")

@csrf_exempt
def process_payment(request):
    print("I pass here before")
    print("add an order here")
    return render(request, "main/donepayment.html")

