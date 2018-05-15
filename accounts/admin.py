from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .models import User
from .forms import UserCreationForm, UserChangeForm


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # These define the fields in the list view
    list_display = ('id', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff',)
    # These are the fields on the 'edit' page
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
    )
    # These are the fields that appear when creating a user via django admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

    def get_readonly_fields(self, request, obj=None):
        # Prevent staff changing their own permissions
        rof = super(UserAdmin, self).get_readonly_fields(request, obj)
        if not request.user.is_superuser:
            rof += ('is_staff', 'is_superuser', 'user_permissions')
        return rof

    def has_change_permission(self, request, obj=None):
        # Prevent staff changing other user's who may have higher privileges.
        has = super(UserAdmin, self).has_change_permission(request, obj)
        if obj and not request.user.is_superuser:
            if obj != request.user:
                if obj.is_superuser or obj.user_permissions.exists():
                    has = False
        return has


# Register user admin
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
