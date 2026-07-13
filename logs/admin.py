from django.contrib import admin
from .models import Log, Entry


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "owner",
        "created_at",
    )

    search_fields = (
        "title",
        "owner__username",
    )

    list_filter = (
        "created_at",
    )


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = (
        "log",
        "short_text",
        "created_at",
    )

    search_fields = (
        "text",
        "log__title",
    )

    list_filter = (
        "created_at",
    )

    def short_text(self, obj):
        return obj.text[:50]