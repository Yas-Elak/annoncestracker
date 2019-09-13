from django.shortcuts import render
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm

from ..models import UserContact
from ..forms import DeuxiemeMainBe
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib import auth
from .tracker_forms import deuxiememainbe_form_call
import random

from ..models import Tracker, Alert
from django.contrib.auth.models import User# Create your views here.


def index(request):
    # What you want the button to do.
    from annoncestracker.settings import BASE_DIR
    current_user = auth.get_user(request)
    invoice_id_part_one = str(current_user.pk)
    invoice_id_part_two = "1"
    invoice_id = invoice_id_part_one + invoice_id_part_two + str(random.randint(0, 1000000))
    paypal_dict = {
        "business": "lakhnati.dv@gmail.com",
        "amount": "5.00",
        "item_name": "gold subscription",
        "invoice": invoice_id,
        "notify_url": request.build_absolute_uri(reverse('main:paypal-ipn')),
        "return": request.build_absolute_uri(reverse('main:done_payment')),
        "cancel_return": request.build_absolute_uri(reverse('main:cancel_payment')),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "main/homepage.html", context)


def paypal_test(request):
    # What you want the button to do.
    current_user = auth.get_user(request)
    invoice_id_part_one = str(current_user.pk)
    invoice_id_part_two = "1"
    invoice_id = invoice_id_part_one + invoice_id_part_two
    paypal_dict = {
        "business": "lakhnati.dv@gmail.com",
        "amount": "5.00",
        "item_name": "gold subscription",
        "invoice": invoice_id,
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('main:done_payment')),
        "cancel_return": request.build_absolute_uri(reverse('main:cancel_payment')),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "main/homepage.html", context)

