from django import forms
from django.core.validators import RegexValidator

from tournament.models import Participant

import pycountry

# Generate a sorted list of tuples for country choices
COUNTRIES = sorted([(country.alpha_2, country.name) for country in pycountry.countries], key=lambda x: x[1])


class PaymentForm(forms.Form):
    tournament = forms.IntegerField(widget=forms.HiddenInput())
    payment = forms.FileField(required=False)


class PassportForm(forms.Form):
    passport = forms.FileField(required=True)
    tournament = forms.IntegerField(widget=forms.HiddenInput())

class UserProfileForm(forms.Form):
    date_of_birth = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date', 'placeholder': 'yyyy/mm/dd','class': 'form-control'}
        ),
        input_formats=['%Y-%m-%d'],
        label='Date of Birth',
    )

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Gender',
    )

    full_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Full Name',
    )

    display_name = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Match your ratings list name. 20 characters max."}),
        label='Name in ratings list',
    )

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )

    phone = forms.CharField(
        validators=[phone_regex],
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=17,
        label='Phone Number',
    )

    country = forms.ChoiceField(choices=COUNTRIES, label="Select Country", widget=forms.Select(attrs={'class': 'form-control'}))

