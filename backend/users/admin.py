from django.contrib import admin

from .models import Subscriptions, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email')
    search_fields = ('username',)
    list_filter = ('username', 'email')


@admin.register(Subscriptions)
class SubscriptionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author')
    autocomplete_fields = ('user', 'author')
