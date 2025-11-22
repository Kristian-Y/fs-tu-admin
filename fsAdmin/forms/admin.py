from django.contrib import admin
from django.http import HttpResponse
from openpyxl import Workbook
import requests
from .models import SponsorApplication
from django.conf import settings

DISCORD_WEBHOOK_URL = getattr(settings, "DISCORD_WEBHOOK_URL", None)


@admin.register(SponsorApplication)
class SponsorApplicationAdmin(admin.ModelAdmin):
    list_display = ("company_name", "contact_person_names", "email", "tier", "created_at")
    search_fields = ("company_name", "contact_person_names", "email")
    list_filter = ("tier", "created_at")
    actions = ["export_as_xlsx"]


    def export_as_xlsx(self, request, queryset):
        """Експортира избраните записи в XLSX"""
        wb = Workbook()
        ws = wb.active
        ws.title = "Sponsor Applications"

        # Заглавия
        headers = ["Company Name", "Contact Person", "Email", "Phone", "Tier", "Description", "Created At"]
        ws.append(headers)

        # Данни
        for app in queryset:
            ws.append([
                app.company_name,
                app.contact_person_names,
                app.email,
                app.phone,
                app.tier,
                app.description,
                app.created_at.strftime("%Y-%m-%d %H:%M"),
            ])

        # Визуално форматиране (по желание)
        for col in ws.columns:
            max_length = 0
            col_name = col[0].column_letter
            for cell in col:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            ws.column_dimensions[col_name].width = max_length + 2

        # Отговор
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="sponsor_applications.xlsx"'
        wb.save(response)
        return response

    export_as_xlsx.short_description = "📊 Export as XLSX"
