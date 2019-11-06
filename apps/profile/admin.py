from django.contrib import admin

from apps.profile.models.membership import Membership
from apps.profile.models.profile import Profile
from apps.profile.models.totem import Totem


class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 1


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'nickname', 'last_name', 'email', 'birthday', 'sex', 'phone_number',
                    'bank_account_number', 'totem']
    inlines = [MembershipInline]


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ['profile', 'werkjaar', 'is_leader', 'tak']
    list_filter = ['is_leader', 'tak', 'werkjaar']


class EmptyProfileFilter(admin.SimpleListFilter):

    title = 'dangling totem'
    parameter_name = 'has_profile'

    def lookups(self, request, model_admin):
        return (
            ('no', 'Is dangling'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'no':
            return queryset.filter(profile=None)


@admin.register(Totem)
class TotemAdmin(admin.ModelAdmin):
    list_display = ['kleurentotem', 'voortotem', 'totem']
    list_filter = [EmptyProfileFilter]
