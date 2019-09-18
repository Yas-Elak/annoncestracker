from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


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

