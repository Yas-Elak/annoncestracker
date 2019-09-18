from paypal.standard.ipn.signals import valid_ipn_received


def payment_notification(sender, **kwargs):
    ipn_obj = sender
    print("iiiiiiiiiiipppppppppppnnnnnnnnnnnnn")


valid_ipn_received.connect(payment_notification)

