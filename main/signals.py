from paypal.standard.ipn.signals import valid_ipn_received
from django.shortcuts import get_object_or_404
from paypal.standard.models import ST_PP_COMPLETED

from main.models import UserContact


def payment_notification(sender, **kwargs):
    ipn_obj = sender
    # if ipn_obj.payment_status == ST_PP_COMPLETED:
    # user_contact = UserContact.objects.get(user__id=1)
    # UserContact.objects.filter(id=1).update(sms=0)
    # print(type(ipn_obj))
    # print(ipn_obj)
    # print(ipn_obj.item_namex)
    print("+++++++++++++++++++++++++")
    # print(ipn_obj.receiver_email)
    # print(ipn_obj.mc_gross)
    print("+++++++++++++++++++++++++")

    # print(ipn_obj.payment_date)
    # print(ipn_obj.payment_status)
    # print(ipn_obj.mc_custom)


valid_ipn_received.connect(payment_notification)

