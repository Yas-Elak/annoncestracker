"""annoncestracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include
from main.views import dashboard, tracking, user_auth, alerts, homepage, user, payments, contact, upgrade

app_name = "main"

urlpatterns = [
    # path("", homepage.index, name="homepage"),

    path("faq/", homepage.faq, name="faq"),
    path("mes_infos/", user.index, name="user_info"),
    path("mes_infos/<activation>", user.activate_auto_delete, name="auto_delete_activate"),

    path("tracking/", tracking.index, name="tracking"),
    path("tracking/tracking_deuxiememain_form", tracking.tracking_deuxiememainbe_form,
         name="tracking_deuxiememainbe_form"),

    path("tracking/<alert_type>/<answer>/", tracking.update_alert_info, name="change_type_alerte"),
    path("tracking/pause/", tracking.update_alerte_pause, name="pause_alerte"),
    path("tracking/delete/", tracking.delete, name="delete_alerte_info"),

    path("alerts/<tracker_id>/", alerts.index, name="alerts"),
    path("alerts/delete/<alert_id>", alerts.delete, name="delete_alerte"),
    path("alerts/<tracker_id>/alerts_deuxiememain_form", alerts.alerts_deuxiememainbe_form,
         name="alerts_deuxiememainbe_form"),

    path("dashboard/", dashboard.index, name="dashboard"),

    path("register/", user_auth.create_user, name="register"),
    path("logout/", user_auth.logout_request, name="logout"),
    path("login/", user_auth.login_request, name="login"),

    # activation
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        user_auth.activate, name='activate'),
    path("resent/", user_auth.resent_activation_email, name="resent"),

    # paypal
    url(r'^paypal/', include('paypal.standard.ipn.urls')),
    path("cancel-payment/", payments.cancel_payment, name="cancel_payment"),
    path("process-payment/", payments.process_payment, name="done_payment"),

    # contact
    path("contact/", contact.contact, name="contact"),

    # upgrade
    path("upgrade/", upgrade.index, name="upgrade"),

    # to delete

]



