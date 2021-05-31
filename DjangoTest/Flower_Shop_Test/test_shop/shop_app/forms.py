from django import forms

from .models import Profile


class CartForm(forms.Form):
    number = forms.IntegerField(label='Quantity', min_value=0, max_value=100)


# 表单类用以生成表单
class AddPhotoForm(forms.Form):
    photo = forms.ImageField(required=False)



