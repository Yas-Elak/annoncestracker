from django.contrib import auth
from django.shortcuts import render
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm


# Create your views here.


def index(request):
    current_user = auth.get_user(request)

    paypal_dict_argent = {
        "cmd": "_xclick-subscriptions",
        "business": "lakhnati.dv@gmail.com",
        "a3": "0.10",  # monthly price4
        "currency_code": "EUR",
        "p3": 1,  # duration of each unit (depends on unit)
        "t3": "M",  # duration unit ("M for Month")
        "src": "1",  # make payments recur
        "sra": "1",  # reattempt payment on payment error
        "no_note": "1",  # remove extra notes (optional)
        "item_name": "Argent Subscription",
        "custom": int(current_user.id),
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('done_payment')),
        "cancel_return": request.build_absolute_uri(reverse('cancel_payment')),
    }

    # Create the instance.
    form_argent = PayPalPaymentsForm(initial=paypal_dict_argent, button_type="subscribe")
    paypal_dict_gold = {
        "cmd": "_xclick-subscriptions",
        "business": "sb-oa1np146616@business.example.com",
        "a3": "9.99",  # monthly price4
        "currency_code": "EUR",
        "p3": 1,  # duration of each unit (depends on unit)
        "t3": "M",  # duration unit ("M for Month")
        "src": "1",  # make payments recur
        "sra": "1",  # reattempt payment on payment error
        "no_note": "1",  # remove extra notes (optional)
        "item_name": "Gold Subscription",
        "custom": "cutoooooom",
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('done_payment')),
        "cancel_return": request.build_absolute_uri(reverse('cancel_payment')),
    }

    # Create the instance.
    form_gold = PayPalPaymentsForm(initial=paypal_dict_gold, button_type="subscribe")

    return render(request, "main/upgrade.html", {"form_argent": form_argent, "form_gold": form_gold})
