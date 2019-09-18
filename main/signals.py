from paypal.standard.ipn.signals import valid_ipn_received
from django.shortcuts import get_object_or_404
from paypal.standard.models import ST_PP_COMPLETED

from main.models import UserContact


def payment_notification(sender, **kwargs):
    ipn_obj = sender
    from pprint import pprint
    # if ipn_obj.payment_status == ST_PP_COMPLETED:
    # user_contact = UserContact.objects.get(user__id=1)
    # UserContact.objects.filter(id=1).update(sms=0)
    # print(type(ipn_obj))
    # print(ipn_obj)
    # print(ipn_obj.item_namex)
    print("i tried a connection")
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        print("COMPLETED")
        print(ipn_obj.custom)
        # print(ipn_obj.item_name)
        # print(ipn_obj.payer_id)
        # print(ipn_obj.txn_id)
    print("+++++++++++++++++++++++++")
    #interessnt
    # payment_status string
    # created_at datetime datetime
    # custom string
    # item_name string
    # payer_id string
    # txn_id
    #

    # print(ipn_obj.payment_date)
    # print(ipn_obj.payment_status)


valid_ipn_received.connect(payment_notification)

