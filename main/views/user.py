from django.shortcuts import render
from ..models import UserContact
from ..forms import DeuxiemeMainBe
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib import auth
from .tracker_forms import deuxiememainbe_form_call

from ..models import Tracker, Alert
from django.contrib.auth.models import User# Create your views here.


def index(request):
    current_user = auth.get_user(request)
    user_contact = UserContact.objects.get(user__id=current_user.id)
    return render(request, "main/user.html", {"user_contact": user_contact, "current_user": current_user})

