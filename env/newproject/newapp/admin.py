from django.contrib import admin
from .models import *
from django.contrib import admin
from django.utils.safestring import mark_safe
admin.site.register(User)
admin.site.register(UserRole)
admin.site.register(Role)
admin.site.register(EventLog)
admin.site.register(SystemConfiguration)
class CameraFeedAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'status', 'is_streaming', 'added_by')
    readonly_fields = ('preview_feed',)
    list_filter = ('status', 'is_streaming', 'location') 
    search_fields = ('name', 'location')  

    def preview_feed(self, obj):
        if obj.feed_url:
            return mark_safe(f'<iframe src="{obj.feed_url}" width="640" height="480" frameborder="0" allowfullscreen></iframe>')
        return "No feed available"

    preview_feed.short_description = "Live Feed Preview"

admin.site.register(CameraFeed, CameraFeedAdmin)



