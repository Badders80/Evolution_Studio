from django.contrib import admin
from .models import Lease


@admin.register(Lease)
class LeaseAdmin(admin.ModelAdmin):
    list_display = ("syndicate_name", "status", "horse", "start_date", "lease_months")
    list_filter = ("status", "horse", "trainer")

    class Media:
        js = ("studio_leases/js/syndicate_naming.js",)
        css = {
            "all": ("studio_leases/css/admin_layout.css",)
        }
