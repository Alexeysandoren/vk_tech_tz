from django.contrib import admin

from friends.models import Friends


@admin.register(Friends)
class FriendsAdmin(admin.ModelAdmin):
    list_display = ['friend_request_receiver', 'friend_request_sender']
