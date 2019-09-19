from django.contrib import auth
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _

from .tracker_forms import deuxiememainbe_form_call
from ..constantes import *
from ..forms import DeuxiemeMainBe
from ..models import Tracker, Alert
from ..models import UserContact


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
    return redirect("tracking")


def update_alerte_pause(request):
    if request.method == 'POST':
        alert_id = int(request.POST.get('alert_id'))
        tracker = Tracker.objects.get(id=alert_id)
        if tracker.activated == "yes":
            Tracker.objects.filter(id=alert_id).update(activated="no")
        else:
            Tracker.objects.filter(id=alert_id).update(activated="yes")
    return redirect("tracking")


def delete(request):
    if request.method == 'POST':
        alert_id = int(request.POST.get('alert_id'))
        alert = Tracker.objects.get(id=alert_id)
        messages.success(request, _(f"{alert.search_query} : supprimé"))
        alert.delete()

    return redirect("tracking")


def delete_all_alerts(request):
    if request.method == 'POST':
        current_user = auth.get_user(request)
        Alert.objects.filter(user_id=current_user.pk).delete()
        messages.success(request, _(f"Toutes les alertes sont supprimées"))

    return redirect("tracking")

def delete_all_alerts_of_tracker(request, tracker_id):
    if request.method == 'POST':
        current_user = auth.get_user(request)
        Alert.objects.filter(user_id=current_user.pk, tracker_id=tracker_id).delete()
        messages.success(request, _(f"Toutes les alertes sont supprimées"))

    return redirect("alerts", tracker_id=tracker_id)


