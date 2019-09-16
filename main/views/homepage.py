from django.shortcuts import render


def faq(request):

    return render(request, "main/faq.html")


def index(request):

    return render(request, "main/homepage.html")


