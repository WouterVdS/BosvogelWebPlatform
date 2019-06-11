from django.contrib import admin

from apps.profile.models.membership import Membership
from apps.profile.models.profile import Profile
from apps.profile.models.totem import Totem


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'nickname', 'last_name', 'email', 'birthday', 'sex', 'phone_number',
                    'bank_account_number', 'totem', 'active']


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ['profile', 'werkjaar', 'is_leader', 'tak', 'is_groupleader']
    list_filter = ['werkjaar', 'tak', 'is_leader']


@admin.register(Totem)
class TotemAdmin(admin.ModelAdmin):
    list_display = ['kleurentotem', 'voortotem', 'totem']
