from django.contrib import admin
from advertisements.models import Advertisement

@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ['title', 'creator', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['title', 'description']