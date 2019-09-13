from django.utils import timezone
from django.shortcuts import render
from ..models import UserContact, Tracker, Alert
from ..forms import UpdateUserContactForm
from django.contrib import auth
from ..constantes import *
from django.http import HttpResponse


# Create your views here.


def index(request):
    current_user = auth.get_user(request)
    user_contact = UserContact.objects.get(user__id=current_user.id)
    number_of_tracker = Tracker.objects.filter(user__id=current_user.id).count()

    number_of_tracker_activated = Tracker.objects.filter(user__id=current_user.id, activated="yes").count()
    number_of_tracker_not_activated = Tracker.objects.filter(user__id=current_user.id, activated="no").count()

    number_of_archives = Alert.objects.filter(user__id=current_user.id).count()

    time_24_hours_ago = timezone.now() - timezone.timedelta(days=1)
    last_24 = Alert.objects.filter(user__id=current_user.id, alert_time__gte=time_24_hours_ago, activated=True).count()

    form = UpdateUserContactForm(initial={'phone_number': user_contact.phone_number,
                                          'email_one': user_contact.email_one,
                                          'email_two': user_contact.email_two})

    return render(request,
                  "main/dashboard.html",
                  {"form": form, "number_of_tracker": number_of_tracker,
                   "user_contact": user_contact,
                   "number_of_archives": number_of_archives,
                   "number_of_tracker_activated": number_of_tracker_activated,
                   "number_of_tracker_not_activated": number_of_tracker_not_activated,
                   "last_24": last_24
                   })
