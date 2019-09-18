from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from paypal.standard.ipn.signals import valid_ipn_received
from django.shortcuts import get_object_or_404
from paypal.standard.models import ST_PP_COMPLETED

from main.models import UserContact, UserOrder


def payment_notification(sender, **kwargs):
    print("I try a connection")
    ipn_obj = sender
    user = User.objects.get(id=int(ipn_obj.custom))
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        if ipn_obj.receiver_email != "sb-oa1np146616@business.example.com":
            a = 0
            print("I'm connected and it's not valid")
            return a
        print("it is valid, I trie to get the order")
        order_exist = UserOrder.objects.filter(user__id=user.pk, pending=1).exist()

        if order_exist:
            print("ok the order exist")
            order = UserOrder.objects.filter(user__id=user.pk, pending=1).order_by('-created').first().update(
                paypal_payer_id=ipn_obj.payer_id, paypal_order_id=ipn_obj.txn_id, product=ipn_obj.item_name, payed=1,
                pending=0, cancelled=0)
        else:
            print("well the order did'nt exist")
            order = UserOrder.objects.create(user=user, paypal_payer_id=ipn_obj.payer_id,
                              paypal_order_id=ipn_obj.txn_id,
                              product=ipn_obj.item_name, payed=1, pending=0, cancelled=0)

        if ipn_obj.item_name == "Gold Subscription":
            print("maintenant je get le item name, ici c'est gold")
            UserContact.objects.get(user__id=user.pk).update(normal_user=0, premium_user=0, super_premium_user=1)
        else:
            print("maintenant je get le item name, ici c'est argent")
            UserContact.objects.get(user__id=user.pk).update(normal_user=0, premium_user=0, super_premium_user=1)
        print("c'est pas tout ça mais on envoie l'email")
        mail_subject = f'Trackannonces thank you for your order.'
        message = render_to_string('main/email/contact_email.html', {
            'subscription': ipn_obj.item_name,
        })
        to_email = user.email
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()


valid_ipn_received.connect(payment_notification)
