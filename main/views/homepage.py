from django.http import HttpResponse
from django.shortcuts import render


def faq(request):

    # return render(request, "main/faq.html")
    return HttpResponse(status=500)


def index(request):
    return render(request, "main/homepage.html")


