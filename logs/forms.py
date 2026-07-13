from django import forms
from .models import Entry
from .models import Log


class LogForm(forms.ModelForm):

    class Meta:
        model = Log

        fields = ["title"]

        labels = {
            "title": "",
        }

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "Log title"
                }
            )
        }

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ["text"]
        labels = {
            "text": "",
        }

        widgets = {
            "text": forms.Textarea(attrs={"cols": 80}),
        }