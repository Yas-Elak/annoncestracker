from ..models import UserContact, Alert, Tracker
from ..forms import DeuxiemeMainBe
from django.contrib import messages
from django.contrib import auth
from django.utils.translation import gettext as _
from ..constantes import *

def deuxiememainbe_form_call(request):
    current_user = auth.get_user(request)
    user_contact = UserContact.objects.get(user__id=current_user.id)
    number_of_tracker = Tracker.objects.filter(user__id=current_user.id).count()
    if request.method == "POST":
        deuxiememainbe_form = DeuxiemeMainBe(request.POST)
        if deuxiememainbe_form.is_valid():
            # ds pour distance meters parce que je peuxpas mettre none dans le choice field
            #Donc si form = 0 alors ds = None
            ds = deuxiememainbe_form.data['distance_meters']
            if deuxiememainbe_form.data['distance_meters'] is "0":
                 ds = None
            if (user_contact.super_premium_user and number_of_tracker < MAX_TRACKERS_GOLD) or\
                    (user_contact.premium_user and number_of_tracker < MAX_TRACKERS_ARGENT) or\
                    (user_contact.normal_user and number_of_tracker < MAX_TRACKERS_NORMAL):
                alert_info = Tracker.objects.create(user_id=current_user.id,
                                                    website="www.2ememain.be",
                                                    search_query=deuxiememainbe_form.data['search_query'],
                                                    distance_meters=ds,
                                                    postal_code=deuxiememainbe_form.data['postal_code'],
                                                    sms=deuxiememainbe_form.data['sms'],
                                                    email=deuxiememainbe_form.data['email'])
                messages.success(request, f"{alert_info.search_query} : created")
            else:
                messages.info(request, _("Vous n'avez plus droit à des trackers, Upgradez pour en avoir plus"))
        else:
            for msg in deuxiememainbe_form.error_messages:
                messages.error(request, f"{msg}:{deuxiememainbe_form.error_messages[msg]}")


