from django import forms
from .models import UserProfile


class UserProfileAdminForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = "__all__"
