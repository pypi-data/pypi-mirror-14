from django.contrib import admin

from .models import AdSense


class AdSenseAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "percentage",
        "ad_client",
        "ad_slot",
        "active",
        "suspended",
        "updated_at",
    ]
admin.site.register(AdSense, AdSenseAdmin)
