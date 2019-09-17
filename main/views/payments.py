from django.contrib.sites import requests
from django.http import HttpResponse
from django.shortcuts import render


def cancel_payment(request):
    print(request)
    print("cancel_payment")
    return render(request, "main/cancelpayment.html")


def process_payment(request):
    print(request)
    print("process payment")
    tx = request.REQUEST['tx']
    print("---------------------------")
    print(tx)
    print("---------------------------")
    return render(request, "main/donepayment.html")


def paypal_ipn(request):
    if request.method == 'POST':
        print("ipppppnnnnnnnnn")
    return HttpResponse('<h1>Page was found</h1>')

#
# class IPNHandler1(webapp.RequestHandler):
#     def post(self):
#         parameters = None
#         # Check payment is completed, not Pending or Failed.
#         if self.request.get('payment_status') == 'Completed':
#             if self.request.POST:
#                 parameters = self.request.POST.copy()
#             if self.request.GET:
#                 parameters = self.request.GET.copy()
#
#
#             if __name__ == '__main__':
#                 print("IPNHandler1 is being run as main().")