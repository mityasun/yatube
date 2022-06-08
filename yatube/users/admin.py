from django.contrib import admin

from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'city')
    search_fields = ('user', 'city')
    list_filter = ('city',)
    empty_value_display = '-пусто-'


admin.site.register(Profile, ProfileAdmin)
