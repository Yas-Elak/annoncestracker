from django.http import HttpResponseRedirect
from django.shortcuts import render
from ..models import UserContact
from ..forms import DeuxiemeMainBe
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib import auth
from .tracker_forms import deuxiememainbe_form_call
from django.utils.translation import gettext as _
from ..constantes import *
from ..models import Tracker, Alert
from django.contrib.auth.models import User# Create your views here.


def index(request):
    current_user = auth.get_user(request)
    deuxiememainbe_form = DeuxiemeMainBe
    user_contact = UserContact.objects.get(user__id=current_user.id)
    tracker_by_date = Tracker.objects.filter(user__id=current_user.id).order_by('-created')
    if user_contact.normal_user:
        all_alerts = Alert.objects.filter(user__id=current_user.id, activated=True).order_by('-alert_time')[:MAX_ARCHIVES_NORMAL]
    elif user_contact.premium_user:
        all_alerts = Alert.objects.filter(user__id=current_user.id, activated=True).order_by('-alert_time')[:MAX_ARCHIVES_ARGENT]
    elif user_contact.super_premium_user:
        all_alerts = Alert.objects.filter(user__id=current_user.id, activated=True).order_by('-alert_time')[:MAX_ARCHIVES_GOLD]
    return render(request,
                  "main/tracking.html",
                  {"deuxiememainbe_form": deuxiememainbe_form, "tracker_by_date": tracker_by_date, "all_alerts": all_alerts, "user_contact": user_contact})


def tracking_deuxiememainbe_form(request):
    deuxiememainbe_form_call(request)
    return index(request)


def update_alert_info(request, alert_type, answer):
    if request.method == 'POST':
        alert_id = int(request.POST.get('alert_id'))
        if alert_type == "sms":
            Tracker.objects.filter(id=alert_id).update(sms=answer)
        else:
            Tracker.objects.filter(id=alert_id).update(email=answer)
    return redirect("main:tracking")


def update_alerte_pause(request):
    if request.method == 'POST':
        alert_id = int(request.POST.get('alert_id'))
        alert = Tracker.objects.get(id=alert_id)
        if alert.activated == "yes":
            Tracker.objects.filter(id=alert_id).update(activated="no")
        else:
            Tracker.objects.filter(id=alert_id).update(activated="yes")
    return redirect("main:tracking")


def delete(request):
    if request.method == 'POST':
        alert_id = int(request.POST.get('alert_id'))
        alert = Tracker.objects.get(id=alert_id)
        messages.success(request, _(f"{alert.search_query} : supprimé"))
        alert.delete()

    return redirect("main:tracking")


