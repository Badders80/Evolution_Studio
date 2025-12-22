from django.contrib import admin
from django.utils.html import format_html
from .models import ContentBlock, MediaAsset, Update


@admin.register(Update)
class UpdateAdmin(admin.ModelAdmin):
    list_display = ("title_link", "published_date", "public_url")
    list_filter = ("update_type", "primary_horse")
    search_fields = ("title", "slug")
    readonly_fields = ("rendered_html_preview",)
    fields = (
        "public_url",
        "rendered_html_preview",
    )

    def rendered_html_preview(self, obj):
        if not obj.rendered_html:
            return "-"
        return format_html(
            '<iframe title="Content Preview" scrolling="no" style="display: block; width: 460px; max-width: calc(100% - 24px); height: 2200px; margin: 0 12px; border: 1px solid #ddd; overflow: hidden;" srcdoc="{}"></iframe>',
            obj.rendered_html,
        )

    rendered_html_preview.short_description = "Preview"

    def title_link(self, obj):
        if obj.public_url:
            return format_html('<a href="{}" target="_blank">{}</a>', obj.public_url, obj.title)
        return format_html('<a href="/admin/studio_content/update/{}/change/">{}</a>', obj.pk, obj.title)

    title_link.short_description = "Title"


@admin.register(MediaAsset)
class MediaAssetAdmin(admin.ModelAdmin):
    list_display = ("name", "published_date", "horse_name", "view_link")
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

    def horse_name(self, obj):
        if not obj.source_update_id:
            return "-"
        primary = getattr(obj.source_update, "primary_horse", None)
        if primary:
            return primary.name
        first = obj.source_update.horses.first()
        return first.name if first else "-"

    horse_name.short_description = "Horse"

    def view_link(self, obj):
        link = obj.public_url or obj.url
        if not link:
            return "-"
        return format_html('<a href="{}" target="_blank">↗</a>', link)

    view_link.short_description = "View"
