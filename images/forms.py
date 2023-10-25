from django import forms
from django.contrib import admin
from .models import UserProfile, Tier


class UserProfileAdminForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'


class TierAdminForm(forms.ModelForm):
    class Meta:
        model = Tier
        fields = '__all__'
