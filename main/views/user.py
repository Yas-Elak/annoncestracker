from django.contrib import auth
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect

from ..models import UserContact

@login_required
def index(request):
    """
    Get the basic info of the user to display at the user
    :param request:
    :return:
    """
    user = auth.get_user(request)
    user_contact = UserContact.objects.get(user__id=user.id)
    form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect("user_info")
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, "main/user.html", {"user_contact": user_contact, "current_user": user, "form":form})

@login_required
def activate_auto_delete(request, activation):
    """
    An option to auto-delete the alerts. Like that the tracker will not pause automatically
    :param request:
    :param activation:
    :return:
    """
    current_user = auth.get_user(request)
    if activation == "activation":
        UserContact.objects.filter(user_id=current_user.id).update(auto_delete=True)
    else:
        UserContact.objects.filter(user_id=current_user.id).update(auto_delete=False)

    return index(request)

