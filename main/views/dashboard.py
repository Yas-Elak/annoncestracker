from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone

from ..forms import UpdateUserContactForm
from ..models import UserContact, Tracker, Alert


# Create your views here.

@login_required
def index(request):
    """
    Get the dashboard of the user with different information like the number of trackers, the archives the result
    and the possibility to get the alert on another email
    :param request:
    :return:
    """
    current_user = auth.get_user(request)
    user_contact = UserContact.objects.get(user__id=current_user.id)

    #Count the total number of tracker owned by the user
    number_of_tracker = Tracker.objects.filter(user__id=current_user.id).count()

    #Count the number of tracker activated and not activated
    number_of_tracker_activated = Tracker.objects.filter(user__id=current_user.id, activated="yes").count()
    number_of_tracker_not_activated = Tracker.objects.filter(user__id=current_user.id, activated="no").count()

    #count the number of archives
    number_of_archives = Alert.objects.filter(user__id=current_user.id, activated=1).count()

    #Get the last alerts in the last 24 hours
    time_24_hours_ago = timezone.now() - timezone.timedelta(days=1)
    last_24 = Alert.objects.filter(user__id=current_user.id, alert_time__gte=time_24_hours_ago, activated=True).count()

    #A from to add an email address where to send the alers
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
