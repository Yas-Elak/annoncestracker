from django import db
from django.shortcuts import render


def faq(request):

    return render(request, "main/faq.html")


def index(request):
    db.connections.close_all()
    return render(request, "main/homepage.html")


