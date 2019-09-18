from paypal.standard.ipn.signals import valid_ipn_received

from main.models import UserContact


def payment_notification(sender, **kwargs):
    ipn_obj = sender
    # user_contact = UserContact.objects.get(user__id=1)
    UserContact.objects.filter(id=1).update(sms=1)
    print("iiiiiiiiiiipppppppppppnnnnnnnnnnnnn")


valid_ipn_received.connect(payment_notification)

