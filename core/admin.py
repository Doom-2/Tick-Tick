from django.contrib import admin
from django.contrib.auth.models import Group

from core.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "first_name", "last_name", )
    search_fields = ("email", "first_name", "last_name", "username", )
    list_filter = ("is_staff", "is_active", "is_superuser", )
    exclude = ("password", "user_permissions", "groups")
    readonly_fields = ("last_login", "date_joined", )


admin.site.unregister(Group)
