from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _

from main.views.tracker_forms import deuxiememainbe_form_call
from ..constantes import *
from ..forms import DeuxiemeMainBe
from ..models import Tracker, Alert
from ..models import UserContact


@login_required
def index(request, tracker_id):
    """

    :param request:
    :param tracker_id:
    :return: The list of the alerts from the tracker find with the tracker ID
    """
    current_user = auth.get_user(request)
    user_contact = UserContact.objects.get(user__id=current_user.id)

    #We get the form because it will be on the page
    deuxiememainbe_form = DeuxiemeMainBe

    #we will show a certain number of alerts set by the role of the users
    if user_contact.super_premium_user:
        all_alerts = Alert.objects.filter(user__id=current_user.id, activated=True).order_by('-alert_time')[:MAX_ARCHIVES_GOLD]
    elif user_contact.premium_user:
        all_alerts = Alert.objects.filter(user__id=current_user.id, activated=True).order_by('-alert_time')[:MAX_ARCHIVES_ARGENT]
    elif user_contact.normal_user:
        all_alerts = Alert.objects.filter(user__id=current_user.id, activated=True).order_by('-alert_time')[:MAX_ARCHIVES_NORMAL]
    tracker = Tracker.objects.get(id=tracker_id)

    return render(request,
                  "main/alerts.html",
                  {"deuxiememainbe_form": deuxiememainbe_form, "all_alerts": all_alerts, "tracker": tracker, "user_contact": user_contact})


@login_required
def alerts_deuxiememainbe_form(request, tracker_id):
    """
    Called when the user use the form deuxiememain
    use the method in the tracker_forms.py
    :param request:
    :param tracker_id:
    :return:
    """
    deuxiememainbe_form_call(request)
    index(request, tracker_id)

@login_required
def delete(request, alert_id):
    """
    Delete the alert choosen by the user
    :param request:
    :param alert_id:
    :return: Redirect to the page alert
    """
    if request.method == 'POST':
        alert = Alert.objects.get(pk=alert_id)
        tracker_id = alert.tracker.id
        Alert.objects.filter(id=alert.id).update(activated=0)
        messages.success(request, _(f"{alert.alert_title} : supprimé"))

    return redirect("alerts", tracker_id=tracker_id)


