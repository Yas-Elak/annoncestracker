from django.contrib import auth
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from main.models import UserOrder

@csrf_exempt
def cancel_payment(request):
    print(request)
    print("cancel_payment")
    return render(request, "main/cancelpayment.html")

@csrf_exempt
def process_payment(request):
    current_user = auth.get_user(request)
    pending = UserOrder.objects.filter(user__id=current_user.pk, pending=1).exists()
    if not pending:
        order = UserOrder.objects.create(user_id=current_user.pk)
    return render(request, "main/donepayment.html")

