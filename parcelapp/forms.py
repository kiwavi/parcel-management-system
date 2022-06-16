from django import forms
from .models import Parcel

class ParcelForm(forms.ModelForm):
    class Meta:
        model = Parcel
        exclude = ['parcel_number','status','status_alert']

class SearchParcelForm(forms.Form):
    parcel_number = forms.IntegerField()

class DischargeForm(forms.Form):
    None

class AcceptForm(forms.Form):
    None
