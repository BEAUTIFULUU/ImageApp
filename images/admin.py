from django.contrib import admin
from .forms import UserProfileAdminForm, TierAdminForm
from .models import UserProfile, Tier


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'account_tier')
    form = UserProfileAdminForm


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Tier)
