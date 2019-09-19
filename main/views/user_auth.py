from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.contrib import messages, auth
from main.custom_email import send_activation_mail
from ..forms import NewUserForm, AuthForm
from ..models import UserContact
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from ..token import account_activation_token
from django.utils.translation import gettext as _



def create_user(request):
    form = NewUserForm
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user_exist = User.objects.filter(email=form.data['email']).exists()
            if user_exist:
                messages.error(request, _("Un utilisateur avec cet email existe déjà"))
            else:
                user = form.save()
                username = form.cleaned_data.get("username")
                user_contact = UserContact(email_one=form.cleaned_data.get("email"), user=user)
                user_contact.save()

                #Confirmation email logique
                send_activation_mail(user, get_current_site(request).domain, form.cleaned_data.get('email'))

                messages.success(request, _(f"Nouveau compte crée: {username}"))
                login(request, user)
                messages.info(request, _(f"Vous êtes maintenant connecté : {username}"))
                messages.info(request, _("Enregistrez votre email afin de pouvoir créer des trackers"))

                return redirect("homepage")
        else:
            data = {'username': form.data['username'], 'email': form.data['email']}
            form = NewUserForm(data)
            for msg in form.error_messages:
                messages.error(request, f"{msg}:{form.error_messages[msg]}")
    return render(request,
                  "main/register.html",
                  {"form": form})


def login_request(request):
    form = AuthForm()
    if request.method == "POST":
        form = AuthForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = User.objects.get(email=email)
            if user is not None and user.check_password(password):
                login(request, user)
                messages.info(request, _(f"Vous êtes maintenant connecté : {user.username}"))
                return redirect("dashboard")
            else:
                messages.error(request, _("Email ou password invalide"))
        else:
            messages.error(request, _("Email ou password invalide"))

    return render(request,
                  "main/login.html",
                  {"form": form})


def logout_request(request):
    logout(request)
    messages.info(request, _("Vous êtes maintenant déconnecté"))
    return redirect("homepage")


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        UserContact.objects.filter(user_id=user.id).update(trackers_activated=1)

        messages.info(request, _("Votre email est confirmé, merci"))
        return redirect("homepage")
    else:
        messages.info(request, _("Lien d'activation invalide"))
        return redirect("homepage")

@login_required
def resent_activation_email(request):
    current_user = auth.get_user(request)
    send_activation_mail(current_user, get_current_site(request).domain, current_user.email)
    messages.info(request, _(f"Email de vérification envoyé, vérifiez vos emails"))
    return redirect("dashboard")


