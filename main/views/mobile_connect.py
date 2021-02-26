from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import random, string
from ..models import UserContact, Alert, Tracker
from django.contrib import auth
from django.utils.translation import gettext as _
from django.core import serializers

from ..constantes import *

def jsontest(request):
    data = {
        'name': 'Vitor',
        'location': 'Finland',
        'is_active': True,
        'count': 28
    }
    return JsonResponse(data)

@login_required
def apiKeyIndex(request):

    current_user = auth.get_user(request)
    user_contact = UserContact.objects.get(user__id=current_user.id)

    key = user_contact.key_api_mobile

    if not key:
        key = _("Vous n'avez pas encore de clé.")

    return render(request, "main/mobile-app-key.html", {"key_api": key})


def generateKey(request):
    current_user = auth.get_user(request)
    user_contact = UserContact.objects.get(user__id=current_user.id)

    #does the same key exist somewhere else?
    key = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10))

    #add the user_contact id like that the key will always be unique
    key += str(user_contact.id)

    user_contact.key_api_mobile = key
    user_contact.save()
    return redirect('api_key_index')


def trackersJson(request, api_key):

    user_contact = UserContact.objects.get(key_api_mobile=api_key)
    tracker_by_date = Tracker.objects.filter(user__id=user_contact.user.id).order_by('-created')

    data = list(tracker_by_date.values())

    #serialized_obj = serializers.serialize('json', [all_alerts, ])

    return JsonResponse(data, safe=False)

def alertsJson(request, api_key, tracker_id):

    user_contact = UserContact.objects.get(key_api_mobile=api_key)
    tracker = Tracker.objects.get(id=tracker_id)


    if user_contact.super_premium_user:
        all_alerts = Alert.objects.filter(user__id=user_contact.user.id, activated=True, tracker=tracker).order_by('-alert_time')[:MAX_ARCHIVES_GOLD]
    elif user_contact.premium_user:
        all_alerts = Alert.objects.filter(user__id=user_contact.user.id, activated=True, tracker=tracker).order_by('-alert_time')[:MAX_ARCHIVES_ARGENT]
    elif user_contact.normal_user:
        all_alerts = Alert.objects.filter(user__id=user_contact.user.id, activated=True, tracker=tracker).order_by('-alert_time')[:MAX_ARCHIVES_NORMAL]

    data = list(all_alerts.values())

    #serialized_obj = serializers.serialize('json', [all_alerts, ])

    return JsonResponse(data, safe=False)


def keyVerification(request, api_key):

    if UserContact.objects.filter(key_api_mobile=api_key).exists():
        data = {
            'key_verification': True
        }
    else:
        data = {
            'key_verification': False
        }

    return JsonResponse(data)
