from paypal.standard.ipn.signals import valid_ipn_received
from django.shortcuts import get_object_or_404
from paypal.standard.models import ST_PP_COMPLETED

from main.models import UserContact


def payment_notification(sender, **kwargs):
    ipn_obj = sender
    print("i tried a connection")
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        print("COMPLETED")
        print(ipn_obj.custom)
        print(ipn_obj.payer_id)
        print(ipn_obj.txn_id)
    print("+++++++++++++++++++++++++")



valid_ipn_received.connect(payment_notification)

