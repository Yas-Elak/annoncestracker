from django.shortcuts import render


def faq(request):
    """
    fctto return the faq
    :param request:
    :return: the FAQ
    """
    return render(request, "main/faq.html")


def index(request):
    """
    fctto return the homepage
    :param request:
    :return: the homepage
    """
    return render(request, "main/homepage.html")


