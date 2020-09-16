from django.shortcuts import render_to_response, render
from django.template import RequestContext


def handler404(request, exception, template_name="main/custom_error/404.html"):
    """Handle 404 error and return appropriate template"""
    response = render_to_response("main/custom_error/404.html")
    response.status_code = 404
    return response

