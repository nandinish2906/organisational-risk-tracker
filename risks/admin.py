from django.contrib import admin
from .models import Risk


@admin.register(Risk)
class RiskAdmin(admin.ModelAdmin):
    list_display = ("risk_id", "title", "category", "risk_score", "risk_level", "status", "owner")
    list_filter = ("category", "risk_level", "status")
    search_fields = ("risk_id", "title", "description", "owner")
    readonly_fields = ("risk_id", "risk_score", "risk_level", "created_at", "updated_at")
