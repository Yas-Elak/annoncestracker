from django.utils import timezone
from django.shortcuts import render
from ..models import UserContact, Tracker, Alert
from ..forms import UpdateUserContactForm
from django.contrib import auth

from django.http import HttpResponse


# Create your views here.


def index(request):

    return render(request, "main/upgrade.html",)
