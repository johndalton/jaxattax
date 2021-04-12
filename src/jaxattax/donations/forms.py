from django import forms

from . import models


class DonateForm(forms.Form):
    name = forms.CharField()
    amount = forms.IntegerField(min_value=1)
    page = forms.ModelChoiceField(
        queryset=models.DonatePage.objects.live(),
        widget=forms.HiddenInput(),
    )
    consent = forms.BooleanField(
        label="I consent for my name and donation amount to be listed on this website",
        required=True,
    )
