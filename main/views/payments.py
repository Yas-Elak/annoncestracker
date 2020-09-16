from django.contrib import auth
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from main.models import UserOrder

@csrf_exempt
def cancel_payment(request):
    """
    Called by the paypal lib to know where to go if it's cancelled
    :param request:
    :return:
    """
    print(request)
    print("cancel_payment")
    return render(request, "main/cancelpayment.html")

@csrf_exempt
def process_payment(request):
    """
    Called by the paypal lib to know where to go when it's done
    :param request:
    :return:
    """
    current_user = auth.get_user(request)
    pending = UserOrder.objects.filter(user__id=current_user.pk, pending=1).exists()
    if not pending:
        UserOrder.objects.create(user=current_user)
    return render(request, "main/donepayment.html")

