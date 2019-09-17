from django.contrib import auth
from django.shortcuts import render
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm


# Create your views here.
from main.models import UserContact


def index(request):
    current_user = auth.get_user(request)
    user_contact = UserContact.objects.get(user__id=current_user.id)

    # paypal_dict_argent = {
    #     "cmd": "_xclick-subscriptions",
    #     "business": "lakhnati.dv@gmail.com",
    #     "a3": "4.99",  # monthly price4
    #     "currency_code": "EUR",
    #     "p3": 1,  # duration of each unit (depends on unit)
    #     "t3": "M",  # duration unit ("M for Month")
    #     "src": "1",  # make payments recur
    #     "sra": "1",  # reattempt payment on payment error
    #     "no_note": "1",  # remove extra notes (optional)
    #     "item_name": "Argent Subscription",
    #     "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
    #     "return": request.build_absolute_uri(reverse('done_payment')),
    #     "cancel_return": request.build_absolute_uri(reverse('cancel_payment')),
    # }
    #
    # # Create the instance.
    # form_argent = PayPalPaymentsForm(initial=paypal_dict_argent, button_type="subscribe")
    # paypal_dict_gold = {
    #     "cmd": "_xclick-subscriptions",
    #     "business": "lakhnati.dv@gmail.com",
    #     "a3": "9.99",  # monthly price4
    #     "currency_code": "EUR",
    #     "p3": 1,  # duration of each unit (depends on unit)
    #     "t3": "M",  # duration unit ("M for Month")
    #     "src": "1",  # make payments recur
    #     "sra": "1",  # reattempt payment on payment error
    #     "no_note": "1",  # remove extra notes (optional)
    #     "item_name": "Gold Subscription",
    #     "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
    #     "return": request.build_absolute_uri(reverse('done_payment')),
    #     "cancel_return": request.build_absolute_uri(reverse('cancel_payment')),
    # }
    #
    # # Create the instance.
    # form_gold = PayPalPaymentsForm(initial=paypal_dict_gold, button_type="subscribe")

    return render(request, "main/upgrade.html", {"user_contact":user_contact})
