from django.utils.html import strip_tags

from main.forms import ContactForm
from main.custom_email import send_contact_mail
from django.shortcuts import render, redirect
from django.contrib import messages

from django.template.loader import render_to_string
from django.core import mail
from django.utils.translation import gettext

def contact(request):
    form = ContactForm()
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            name = form.cleaned_data.get("name")
            texte = form.cleaned_data.get("message")
            send_contact_mail(name, email, texte)
            messages.info(request, gettext("Message envoyé"))
            return redirect("homepage")
        else:
            messages.error(request, gettext("Formulaire invalide"))

    return render(request, "main/contact.html", {"form": form})

