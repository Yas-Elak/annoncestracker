from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils import timezone


class UserOrder(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    paypal_payer_id = models.CharField(max_length=255, null=True, blank=True)
    paypal_order_id = models.CharField(max_length=255, null=True, blank=True)
    product = models.CharField(max_length=255, null=True, blank=True)
    payed = models.BooleanField(default=0)
    pending = models.BooleanField(default=1)
    cancelled = models.BooleanField(default=1)
    created = models.DateTimeField(default=timezone.now)


class UserContact(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='user_contact')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email_one = models.EmailField()
    email_two = models.EmailField(blank=True, null=True)
    sms = models.IntegerField(default=0)
    normal_user = models.BooleanField(default=True)
    premium_user = models.BooleanField(default=False)
    super_premium_user = models.BooleanField(default=False)
    auto_delete = models.BooleanField(default=False)
    trackers_activated = models.BooleanField(default=False)

    def __str__(self):
        return f"phone : {self.phone_number} / Email 1 : {self.email_one} / Email 2 : {self.email_two}"


only_title = "Title"
only_content = "Content"
both = "Both"
ALERT_CHOICES = (
    (only_title, "Title"),
    (only_content, "Content"),
    (both, "Both")
)
yes = "yes"
no = "no"
YES_NO_CHOICES = (
    (yes, "yes"),
    (no, "no")
)


deuxieme_main = "www.2ememain.be"
WEBSITE_CHOICES = (
    (deuxieme_main, "www.2ememain.be"),
)

all_distances = "0"
DISTANCES_CHOICES = (
    (all_distances, "all distances"),
    ("3000", "< 3 km"),
    ("5000", "< 5 km"),
    ("10000", "< 10 km"),
    ("15000", "< 15 km"),
    ("25000", "< 25 km"),
    ("50000", "< 50 km"),
    ("75000", "< 75 km")
)


class Tracker(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    website = models.CharField(max_length=200, choices=WEBSITE_CHOICES, default=deuxieme_main)
    search_query = models.CharField(max_length=255)
    distance_meters = models.CharField(max_length=255, choices=DISTANCES_CHOICES, default=all_distances, null=True)
    postal_code = models.CharField(max_length=6, blank=True, null=True)
    exclude_query = models.CharField(max_length=255, blank=True, null=True)
    search_partial = models.CharField(max_length=4, choices=YES_NO_CHOICES, default=no, blank=True, null=True)
    sms = models.CharField(max_length=4, choices=YES_NO_CHOICES, default=no)
    email = models.CharField(max_length=4, choices=YES_NO_CHOICES, default=yes)
    title_content = models.CharField(max_length=9, choices=ALERT_CHOICES, blank=True, null=True)
    activated = models.CharField(max_length=4, choices=YES_NO_CHOICES, default=yes)
    created = models.DateTimeField(default=timezone.now)
    first_time = models.BooleanField(default=True)


class Alert(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    tracker = models.ForeignKey(Tracker, on_delete=models.CASCADE, null=True)
    alert_time = models.DateTimeField(default=timezone.now)
    pseudo_user = models.CharField(max_length=255)
    alert_title = models.TextField()
    alert_content = models.TextField()
    alert_price = models.CharField(max_length=255)
    alert_location = models.CharField(max_length=255)
    alert_url = models.TextField()
    alert_id = models.BigIntegerField(unique=True)
    activated = models.BooleanField(default=True)
    send = models.BooleanField(default=False)

