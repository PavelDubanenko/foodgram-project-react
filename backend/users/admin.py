from django.contrib import admin

from .models import (User, Follow)


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'first_name',
        'last_name',
        'username',
        'email',
    )
    search_fields = ('username',)
    list_filter = ('email', 'first_name')
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
admin.site.register(Follow)
