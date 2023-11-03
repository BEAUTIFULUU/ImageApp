from django.contrib import admin
from .forms import UserProfileAdminForm
from .models import UserProfile, CustomTier


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'account_tier')
    form = UserProfileAdminForm


class TierAdmin(admin.ModelAdmin):

    admin.site.register(UserProfile, UserProfileAdmin)
    admin.site.register(CustomTier)
