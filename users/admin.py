from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# We customize the default UserAdmin to show our new checkboxes
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('EdTech Roles', {'fields': ('is_tutor', 'is_student')}),
    )

admin.site.register(User, CustomUserAdmin)