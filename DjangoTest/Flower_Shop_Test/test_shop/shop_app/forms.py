from django import forms

class CartForm(forms.Form):
    number = forms.IntegerField(label='Quantity', min_value=0, max_value=100)