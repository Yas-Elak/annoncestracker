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
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap

from main.views import dashboard, tracking, user_auth, alerts, homepage, user, payments, contact, upgrade, mobile_connect

from main.sitemaps import Static_Sitemap

#URL should extend the one in the "main" folder, but it will not work with locale if allthe url are not here

sitemaps = {
    'static': Static_Sitemap(),
}

urlpatterns = [
    # path('', include('main.urls')),
    path('admin/', admin.site.urls),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('i18n/', include('django.conf.urls.i18n')),  # Make sure this is present or the set_language url will not be found
]
#
urlpatterns += i18n_patterns(
    path('', homepage.index, name="homepage"),

    path("faq/", homepage.faq, name="faq"),
    path("mes_infos/", user.index, name="user_info"),
    path("mes_infos/<activation>", user.activate_auto_delete, name="auto_delete_activate"),

    path("tracking/", tracking.index, name="tracking"),
    path("tracking/tracking_deuxiememain_form", tracking.tracking_deuxiememainbe_form,
         name="tracking_deuxiememainbe_form"),

    path("tracking/<alert_type>/<answer>/", tracking.update_alert_info, name="change_type_alerte"),
    path("tracking/pause/", tracking.update_alerte_pause, name="pause_alerte"),
    path("tracking/delete/", tracking.delete, name="delete_alerte_info"),
    path("tracking/delete_all/", tracking.delete_all_alerts, name="delete_all_alerts"),
    path("tracking/delete_all/<tracker_id>", tracking.delete_all_alerts_of_tracker,
         name="delete_all_alerts_of_tracker"),

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

    # Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
    # ask for the email
    path('password_change/',
         auth_views.PasswordResetView.as_view(template_name='main/registration/password_change.html',
                                              html_email_template_name='main/email/password_reset_email.html'),
         name='password_reset'),

    # the email is sent and in the maintime we go here
    path('password_reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='main/registration/password_reset_done.html'),
         name='password_reset_done'),

    # then the link in the email is clicked and we go here
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="main/registration/password_reset_confirm.html"),
         name='password_reset_confirm'),

    # then if ok we go tothe confirmation page
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='main/registration/password_reset_complete.html'),
         name='password_reset_complete'),

    #then we say we can log
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),


    #JSON
    path("mobile-app-key/", mobile_connect.apiKeyIndex, name="api_key_index"),
    path("key-generation/", mobile_connect.generateKey, name='generate_key'),
    path("mobile/<str:api_key>/trackers", mobile_connect.trackersJson, name='trackers_json'),
    path("mobile/<str:api_key>/alerts/<int:tracker_id>/", mobile_connect.alertsJson, name='alerts_json'),
    path("mobile/<str:api_key>/verification/", mobile_connect.keyVerification, name='key_verification'),
    #sitemap

    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    # to delete


    path("jsontest/", mobile_connect.jsontest, name="jsontest"),

)

#custom error
handler404 = 'main.views.custom_error.handler404'

