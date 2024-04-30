from django import forms
from .models import Unit, Food, FoodsInStock, Purchases, User, Dish, DishIngredient

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
        model = FoodsInStock
        fields = ['Food', 'Quantity', 'Sum']


class PurchaseForm(forms.ModelForm):
    Date = forms.DateTimeField(
        input_formats=['%Y-%m-%dT%H:%M'],  # Укажите формат даты и времени
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
    )
    class Meta:
        model = Purchases
        fields = ['Title']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['Author'].queryset = User.objects.all()  # Assuming Author field relates to User model
        self.fields['Date'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M')

    def save(self, commit=True):
        instance = super().save(commit=False)
        date = self.cleaned_data.get('Date')
        amount = self.cleaned_data.get('Amount')

        if date and amount:
            title = f"{date.strftime('%Y-%m-%d %H:%M')} - {amount}"  # Format the date without timezone information
            instance.Title = title

        if commit:
            instance.save()
        return instance


class DishForm(forms.ModelForm):

    class Meta:
        model = Dish
        fields = ['Title', 'Author', 'Caloric_value', 'Proteins', 'Fats', 'Carbohydrates', 'Cooking_instructions']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['Author'].queryset = User.objects.all()  # Assuming Author field relates to User model

class DishIngredientsForm(forms.ModelForm):
    class Meta:
        model = DishIngredient
        fields = ['Food', 'Quantity']