from django import forms
from main.models import Author
from django.utils.translation import gettext_lazy as _


class UpdateForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ("fullname", "bio", "profile_pic")
        labels = {
            "fullname": _("Imię i nazwisko"),
            "bio": _("Biogram"),
            "profile_pic": _("Zdjęcie profilowe"),
        }