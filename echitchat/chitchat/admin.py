from django.contrib import admin
from .models import User, Message, Profile, Connection, Group, GroupMember


# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email']


class ProfileAdmin(admin.ModelAdmin):
    list_editable = ['verified']
    list_display = ['user', 'full_name', 'verified']


class MessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'connection', 'group', 'message']


class ConnectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'sender', 'receiver', 'accepted']


class GroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class GroupMemberAdmin(admin.ModelAdmin):
    list_display = ['id', 'group', 'user']


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Connection, ConnectionAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(GroupMember, GroupMemberAdmin)
