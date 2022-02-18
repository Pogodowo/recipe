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

class CzopkiGlobulkiForm (ModelForm):
    class Meta:
        model = Receptura
        fields = ['nazwa', 'rodzaj',
        'czopki_czy_globulk',
        'ilosc_czop_glob' ,
        'masa_docelowa_czop_glob' ,
        'czy_ilosc_oleum_pomnozyc' ,]
        labels = {
            'nazwa': 'tytuł recepty',
        }