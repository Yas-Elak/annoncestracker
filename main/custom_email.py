from django.core import mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from main.token import account_activation_token


def send_contact_mail(name, email, texte):
    mail_subject = f'Trackannonces contact : Message de {name}.'
    html_message = render_to_string('main/email/contact_email.html', {
        'user': name,
        'email': email,
        'texte': texte
    })
    plain_message = strip_tags(html_message)
    to_email = "elalaoui87@gmail.com"
    from_email = 'Trackannonces.be <info@mg.trackannonce.be>'
    mail.send_mail(mail_subject, plain_message, from_email, [to_email], html_message=html_message)


def send_activation_mail(user, current_site_domain, to_email):
    mail_subject = 'Activate your account.'
    html_message = render_to_string('main/email/acc_active_email.html', {
        'user': user,
        'domain': current_site_domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    plain_message = strip_tags(html_message)
    from_email = 'Trackannonces.be <noreply@mg.trackannonce.be>'
    mail.send_mail(mail_subject, plain_message, from_email, [to_email], html_message=html_message)


def send_thank_you_for_subscription(item_name, email, username):
    mail_subject = f'Trackannonces thanks you for your order.'
    html_message = render_to_string('main/email/subscription.html', {
        'subscription': item_name,
        'username': username
    })
    to_email = email
    plain_message = strip_tags(html_message)
    from_email = 'Trackannonces.be <noreply@mg.trackannonce.be>'
    mail.send_mail(mail_subject, plain_message, from_email, [to_email], html_message=html_message)


def send_you_got_paypal_news(type_of_message, username, email, type_off_abo):
    mail_subject = f"""l'utilisateur {username} / {email} {type_of_message}"""
    html_message = render_to_string('main/email/info_subscription.html', {
        'subscription': type_off_abo,
    })
    to_email = "elalaoui87@gmail.com"
    plain_message = strip_tags(html_message)
    from_email = 'Trackannonces.be <info@mg.trackannonce.be>'
    mail.send_mail(mail_subject, plain_message, from_email, [to_email], html_message=html_message)
