from django.contrib import admin

from .models import Channel, Message


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('name', 'unique_hash', 'is_open', 'owner')
    list_filter = ('owner', 'is_open',)
    fieldsets = (
        (None, {'fields': ('name', 'unique_hash', 'is_open', )}),
        ('Dates', {'fields': ('created', 'modified')}),
    )

    search_fields = ('unique_hash',)
    ordering = ('created',)
    readonly_fields = ('created', 'modified')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('owner', 'channel', 'created_at', )
    list_filter = ('owner', 'channel')
    fieldsets = (
        (None, {'fields': ('owner', 'content', 'channel')}),
        ('Dates', {'fields': ('created_at', )}),
    )

    search_fields = ('owner', 'channel')

