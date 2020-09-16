from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from .tracker_forms import deuxiememainbe_form_call
from ..constantes import *
from ..forms import DeuxiemeMainBe
from ..models import Tracker, Alert
from ..models import UserContact


@login_required
def index(request):
    """
    Get the basic info of the tracking page
    The list of trackers
    The list of alerts for all trackers
    A way to create a new tracker
    :param request:
    :return: the tracking page
    """
    current_user = auth.get_user(request)
    deuxiememainbe_form = DeuxiemeMainBe
    user_contact = UserContact.objects.get(user__id=current_user.id)
    tracker_by_date = Tracker.objects.filter(user__id=current_user.id).order_by('-created')
    dict_of_activated_tracker_alerts = {}

    #Count the number of activated alerts for each tracker
    for tracker in tracker_by_date:
        dict_of_activated_tracker_alerts[tracker.id] = Alert.objects.filter(tracker_id=tracker.id, activated=1).count()

    #Display the alerts by role of the user
    if user_contact.normal_user:
        all_alerts = Alert.objects.filter(user__id=current_user.id, activated=True).order_by('-alert_time')[:MAX_ARCHIVES_NORMAL]
    elif user_contact.premium_user:
        all_alerts = Alert.objects.filter(user__id=current_user.id, activated=True).order_by('-alert_time')[:MAX_ARCHIVES_ARGENT]
    elif user_contact.super_premium_user:
        all_alerts = Alert.objects.filter(user__id=current_user.id, activated=True).order_by('-alert_time')[:MAX_ARCHIVES_GOLD]
    return render(request,
                  "main/tracking.html",
                  {"deuxiememainbe_form": deuxiememainbe_form, "dict_of_activated_tracker_alerts": dict_of_activated_tracker_alerts, "tracker_by_date": tracker_by_date, "all_alerts": all_alerts, "user_contact": user_contact})


def tracking_deuxiememainbe_form(request):
    """
    When the form is called.
    :param request:
    :return: the tracking page
    """
    deuxiememainbe_form_call(request)
    return index(request)


def update_alert_info(request, alert_type, answer):
    """
    Note useful now. It's if we have the options to send alert by email and SMS
    :param request:
    :param alert_type:
    :param answer: yes or no
    :return: the tracking page
    """
    if request.method == 'POST':
        alert_id = int(request.POST.get('alert_id'))
        if alert_type == "sms":
            Tracker.objects.filter(id=alert_id).update(sms=answer)
        else:
            Tracker.objects.filter(id=alert_id).update(email=answer)
    return redirect("tracking")

@login_required
def update_alerte_pause(request):
    """
    To put a tracker on pause
    :param request:
    :return: the tracking page
    """
    if request.method == 'POST':
        alert_id = int(request.POST.get('alert_id'))
        tracker = Tracker.objects.get(id=alert_id)
        if tracker.activated == "yes":
            Tracker.objects.filter(id=alert_id).update(activated="no")
        else:
            Tracker.objects.filter(id=alert_id).update(activated="yes")
    return redirect("tracking")

@login_required
def delete(request):
    """
    To delete the alert
    :param request:
    :return:
    """
    if request.method == 'POST':
        alert_id = int(request.POST.get('alert_id'))
        alert = Tracker.objects.get(id=alert_id)
        messages.success(request, _(f"{alert.search_query} : supprimé"))
        alert.delete()

    return redirect("tracking")

@login_required
def delete_all_alerts(request):
    """
    to Delete all alerts whatever the tracker
    :param request:
    :return:
    """
    if request.method == 'POST':
        current_user = auth.get_user(request)
        Alert.objects.filter(user_id=current_user.pk).update(activated=0)
        messages.success(request, _(f"Toutes les alertes sont supprimées"))

    return redirect("tracking")

@login_required
def delete_all_alerts_of_tracker(request, tracker_id):
    """
    To delete alerts of a tracker
    :param request:
    :param tracker_id:
    :return:
    """
    if request.method == 'POST':
        current_user = auth.get_user(request)
        Alert.objects.filter(user_id=current_user.pk, tracker_id=tracker_id).update(activated=0)
        messages.success(request, _(f"Toutes les alertes sont supprimées"))

    return redirect("alerts", tracker_id=tracker_id)


