from django.contrib import auth
from django.http import request
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver
from paypal.standard.models import ST_PP_COMPLETED
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from datetime import datetime

from main.models import UserContact

@receiver(valid_ipn_received)
def ipn_receiver(sender, **kwargs):
    ipn_obj = sender
    print("test")
    current_user = auth.get_user(request)

    user_contact = UserContact.objects.get(user__id=current_user.id)
    UserContact.objects.filter(user_id=1).update(email_two="truc@gmail.com")

    # check for Buy Now IPN
    if ipn_obj.txn_type == 'web_accept':

        if ipn_obj.payment_status == ST_PP_COMPLETED:
            # payment was successful
            print('great!')
            # order = get_object_or_404(Order, id=ipn_obj.invoice)

            # if order.get_total_cost() == ipn_obj.mc_gross:
            #     # mark the order as paid
            #     order.paid = True
            #     order.save()

    # # check for subscription signup IPN
    # elif ipn_obj.txn_type == "subscr_signup":
    #
    #     # get user id and activate the account
    #     id = ipn_obj.custom
    #     user = User.objects.get(id=id)
    #     user.active = True
    #     user.save()
    #
    #     subject = 'Sign Up Complete'
    #
    #     message = 'Thanks for signing up!'
    #
    #     email = EmailMessage(subject,
    #                          message,
    #                          'admin@myshop.com',
    #                          [user.email])
    #
    #     email.send()
    #
    # # # check for subscription payment IPN
    # # elif ipn_obj.txn_type == "subscr_payment":
    # #
    # #     # get user id and extend the subscription
    # #     id = ipn_obj.custom
    # #     user = User.objects.get(id=id)
    # #     # user.extend()  # extend the subscription
    # #
    # #     subject = 'Your Invoice for {} is available'.format(
    # #         datetime.strftime(datetime.now(), "%b %Y"))
    # #
    # #     message = 'Thanks for using our service. The balance was automatically ' \
    # #               'charged to your credit card.'
    # #
    # #     email = EmailMessage(subject,
    # #                          message,
    # #                          'admin@myshop.com',
    # #                          [user.email])
    # #
    # #     email.send()
    #
    # # # check for failed subscription payment IPN
    # # elif ipn_obj.txn_type == "subscr_failed":
    # #     pass
    # #
    # # # check for subscription cancellation IPN
    # # elif ipn_obj.txn_type == "subscr_cancel":
    # #     pass
    # #

valid_ipn_received.connect(ipn_receiver)
