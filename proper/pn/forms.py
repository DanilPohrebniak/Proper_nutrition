from django import forms
from .models import Unit, Food

import datetime


class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['name']


class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ['name']