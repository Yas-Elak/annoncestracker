from main.forms import ContactForm

from django.shortcuts import render, redirect
from django.contrib import messages

from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.translation import gettext

def contact(request):
    form = ContactForm()
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            name = form.cleaned_data.get("name")
            texte = form.cleaned_data.get("message")
            mail_subject = f'Trackannonces contact : Message de {name}.'
            message = render_to_string('main/email/contact_email.html', {
                'user': name,
                'email': email,
                'texte': texte
            })
            to_email = "elalaoui87@gmail.com"
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            messages.info(request, gettext("Message envoyé"))
            return redirect("homepage")
        else:
            messages.error(request, gettext("Formulaire invalide"))

    return render(request, "main/contact.html", {"form": form})

