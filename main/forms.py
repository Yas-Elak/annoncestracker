from django import forms
from .models import UserContact, Tracker
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext as _


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(required=True, min_length=3)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(NewUserForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'email', 'password1', 'password2']:
            self.fields[fieldname].help_text = None


class AuthForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


class UpdateUserContactForm(forms.ModelForm):
    class Meta:
        model = UserContact
        fields = ["email_one", "email_two"]
        labels = {
            "email_one": _("Premier Email"),
            "email_two": _("Deuxième Email")
        }



class DeuxiemeMainBe(forms.ModelForm):
    class Meta:
        model = Tracker

        fields = ["search_query",
                  "postal_code",
                  "distance_meters",
                  "search_partial",
                  "email",
                  ]
        labels = {"search_query": _("Rechercher ce mot / ces mots"),
                  "postal_code": _("Code postal"),
                  "distance_meters": _("Distance depuis le code postal"),
                  "search_partial": _("Mot partiel ou non"),
                  "email": _("Envoyé par email"),
                  }
        widgets = {
            'postal_code': forms.TextInput(
                attrs={'placeholder': 'Ex: 5000',
                       'type': 'number'}
            )
        }


class ContactForm(forms.Form):
    name = forms.CharField(max_length=255)
    email = forms.EmailField(max_length=255)
    message = forms.CharField(widget=forms.Textarea)
    fields = ["name",
              "email",
              "message",
              ]
    labels = {"name": _("Nom"),
              "email": "Email",
              "message": _("Message"),
              }
    message.widget.attrs.update({'class': 'materialize-textarea'})

