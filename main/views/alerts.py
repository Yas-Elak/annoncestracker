from django.shortcuts import render
from ..models import UserContact
from ..forms import DeuxiemeMainBe
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib import auth
from main.views.tracker_forms import deuxiememainbe_form_call
from ..models import Tracker, Alert
from django.contrib.auth.models import User# Create your views here.
from django.utils.translation import gettext as _

def index(request, tracker_id):
    current_user = auth.get_user(request)
    user_contact = UserContact.objects.get(user__id=current_user.id)
    deuxiememainbe_form = DeuxiemeMainBe
    if user_contact.super_premium_user:
        all_alerts = Alert.objects.filter(user__id=current_user.id, activated=True).order_by('-alert_time')[:250]
    elif user_contact.premium_user:
        all_alerts = Alert.objects.filter(user__id=current_user.id, activated=True).order_by('-alert_time')[:25]
    elif user_contact.normal_user:
        all_alerts = Alert.objects.filter(user__id=current_user.id, activated=True).order_by('-alert_time')[:5]
    tracker = Tracker.objects.get(id=tracker_id)

    return render(request,
                  "main/alerts.html",
                  {"deuxiememainbe_form": deuxiememainbe_form, "all_alerts": all_alerts, "tracker": tracker, "user_contact": user_contact})


def alerts_deuxiememainbe_form(request, tracker_id):
    deuxiememainbe_form_call(request)
    index(request, tracker_id)


def delete(request, alert_id):
    if request.method == 'POST':
        alert = Alert.objects.get(pk=alert_id)
        tracker_id = alert.tracker.id
        Alert.objects.filter(id=alert.id).update(activated=0)
        messages.success(request, _(f"{alert.alert_title} : supprimé"))

    return redirect("main:alerts", tracker_id=tracker_id)


# https://codepen.io/marcmatias/pen/gxPzvY