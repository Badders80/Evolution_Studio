from django.contrib import admin
from django.utils.html import format_html
from .models import ContentBlock, MediaAsset, Update


class ContentBlockInline(admin.TabularInline):
    model = ContentBlock
    extra = 0


@admin.register(Update)
class UpdateAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "update_type",
        "primary_horse",
        "race_date",
        "published_date",
        "slug",
    )
    list_filter = ("update_type", "primary_horse", "race_track")
    search_fields = ("title", "slug")
    inlines = [ContentBlockInline]


@admin.register(MediaAsset)
class MediaAssetAdmin(admin.ModelAdmin):
    list_display = ("name", "published_date", "source_update_link", "public_url")
    search_fields = ("name", "public_url")

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(is_finished=True)

    def source_update_link(self, obj):
        if not obj.source_update_id:
            return "-"
        return format_html(
            '<a href="/admin/studio_content/update/{}/change/">{}</a>',
            obj.source_update_id,
            obj.source_update.title,
        )

    source_update_link.short_description = "Content Blocks"
