from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from users.models import UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profile & Address'
    fk_name = 'user'


class CustomUserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_phone', 'date_joined')
    list_select_related = ('profile',)

    def get_phone(self, instance):
        if hasattr(instance, 'profile'):
            return instance.profile.phone_number
        return '-'
    get_phone.short_description = 'Phone Number'


# Re-register UserAdmin with profile inline
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'city', 'state', 'country', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone_number', 'city', 'state')
    list_filter = ('country', 'state', 'created_at')
