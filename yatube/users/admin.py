from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CreationForm
from .models import User


class UserAdmin(UserAdmin):
    add_form = CreationForm
    model = User
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': (
            'first_name',
            'last_name',
            'email',
            'profile_pic',
            'city',
            'vk',
            'telegram',
            'instagram',
            'git'
        )}),
        ('Права', {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions'
        )}),
        ('Даты', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2')}
         ),
    )


admin.site.register(User, UserAdmin)
