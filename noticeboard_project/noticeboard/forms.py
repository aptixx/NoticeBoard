from django import forms
from .models import Advert
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class AdvertForm(forms.ModelForm):
    class Meta:
        model = Advert
        fields = ['category', 'headline', 'text', 'video', 'image']


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)
