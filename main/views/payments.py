import urllib
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sites import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_http_methods
from paypal.standard.pdt.views import process_pdt

from annoncestracker import settings


def cancel_payment(request):
    print(request)
    print("cancel_payment")
    return render(request, "main/cancelpayment.html")

@csrf_exempt
def process_payment(request):
    # print(request)
    # print("process payment")
    # tx = request.GET.get("tx")
    # print("---------------------------")
    # # print(tx)
    # print("---------------------------")
    # result = paypal.Verify(tx)
    # if result.success():  # valid
    #     print("yeeeeeeeeeeeeeeeeeeep")
    return render(request, "main/donepayment.html")


@require_http_methods(["GET", "POST"])
def pdt_paypal(request):
    pdt_obj, failed = process_pdt(request)
    context = {"failed": failed, "pdt_obj": pdt_obj}
    if not failed:
        print("PDT not failed")
        # WARNING!
        # Check that the receiver email is the same we previously
        # set on the business field request. (The user could tamper
        # with those fields on payment form before send it to PayPal)

        if pdt_obj.receiver_email == "receiver_email@example.com":
            print("PDT Same email")
            # ALSO: for the same reason, you need to check the amount
            # received etc. are all what you expect.

            # Do whatever action is needed, then:
            return render(request, 'main/donepayment.html', context)
    return render(request, 'main/cancelpayment.html', context)
