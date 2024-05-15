from django import forms
from .models import Post
from django.utils.translation import gettext_lazy as _


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "categories", "tags"]
        labels = {
            "title": _("Tytuł"),
            "content": _("Treść"),
            "categories": _("Kategorie"),
            "tags": _("Tagi"),
        }
        help_texts = {
            'tags': _('Lista tagów oddzielonych przecinkami.')
        }