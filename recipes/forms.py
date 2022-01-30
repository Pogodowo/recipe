from django import forms
from django.forms import ModelForm
from .models import Receptura

class RecepturaForm (ModelForm):
    class Meta:
        model = Receptura
        fields = ['nazwa', 'rodzaj',]
        labels = {
            'nazwa': 'tytuł recepty',
        }
