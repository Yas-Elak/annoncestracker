from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from paypal.standard.ipn.signals import valid_ipn_received
from main.custom_email import *
from paypal.standard.models import ST_PP_COMPLETED, ST_PP_CANCELLED

from main.models import UserContact, UserOrder


def payment_notification(sender, **kwargs):
    print("I try a connection")
    ipn_obj = sender
    user = User.objects.get(id=int(ipn_obj.custom))

    if ipn_obj.payment_status == ST_PP_CANCELLED:
        user_contact = UserContact.objects.get(user__id=user.id)
        if (user_contact.super_premium_user == 1 and ipn_obj.item_name == "Gold Subscription") or (user_contact.premium_user == 1 and ipn_obj.item_name == "Argent Subscription"):
            UserContact.objects.filter(user__id=user.pk).update(normal_user=1, premium_user=0, super_premium_user=0)
        send_you_got_paypal_news("a annulé son abo", user.username, user.email, ipn_obj.item_name)

    if ipn_obj.payment_status == ST_PP_COMPLETED:
        if ipn_obj.receiver_email != "sb-oa1np146616@business.example.com":
            a = 0
            print("I'm connected and it's not valid")
            return a
        print("it is valid, I try to get the order")
        order_exist = UserOrder.objects.filter(user__id=user.pk, pending=1).exists()

        if order_exist:
            print("ok the order exist")
            order = UserOrder.objects.filter(user__id=user.pk, pending=1).order_by('-created').first()
            order.paypal_payer_id=ipn_obj.payer_id
            order.paypal_order_id=ipn_obj.txn_id
            order.product=ipn_obj.item_name
            order.payed=1
            order.pending=0
            order.cancelled=0
            order.save()
        else:
            print("well the order did'nt exist")
            order = UserOrder.objects.create(user=user, paypal_payer_id=ipn_obj.payer_id,
                              paypal_order_id=ipn_obj.txn_id,
                              product=ipn_obj.item_name, payed=1, pending=0, cancelled=0)

        if ipn_obj.item_name == "Gold Subscription":
            print("maintenant je get le item name, ici c'est gold")
            UserContact.objects.filter(user__id=user.pk).update(normal_user=0, premium_user=0, super_premium_user=1)
        else:
            print("maintenant je get le item name, ici c'est argent")
            UserContact.objects.filter(user__id=user.pk).update(normal_user=0, premium_user=1, super_premium_user=0)
        print("c'est pas tout ça mais on envoie l'email")

        send_thank_you_for_subscription(ipn_obj.item_name,user.email, user.username)
        send_you_got_paypal_news("a fait une commande", user.username, user.email, ipn_obj.item_name)


valid_ipn_received.connect(payment_notification)
