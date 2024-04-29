from django import forms
from .models import Unit, Food, Foods_in_stock, Purchases, User

import datetime


class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['name']


class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ['name', 'unit']


class FoodsInStockForm(forms.ModelForm):
    class Meta:
        model = Foods_in_stock
        fields = ['Food', 'Quantity', 'Sum']


class PurchaseForm(forms.ModelForm):
    Date = forms.DateTimeField(
        input_formats=['%Y-%m-%dT%H:%M'],  # Укажите формат даты и времени
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
    )
    class Meta:
        model = Purchases
        exclude = ['Title']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add select fields for Author, Warehouse, Counterparty
        self.fields['Author'].queryset = User.objects.all()  # Assuming Author field relates to User model
        self.fields['Date'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M')

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('Date')
        amount = cleaned_data.get('Amount')

        if date and amount:
            title = f"{date} - {amount}"
            cleaned_data['Title'] = title

        return cleaned_data
