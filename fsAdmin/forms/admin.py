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

    def save_model(self, request, obj, form, change):
        """При нов запис пращаме Discord известие"""
        super().save_model(request, obj, form, change)

        if not change and DISCORD_WEBHOOK_URL:
            embed = {
                "title": "🆕 Нова спонсорска заявка!",
                "color": 0xFFD700 if obj.tier == "gold" else 0xC0C0C0 if obj.tier == "silver" else 0xCD7F32 if obj.tier == "bronze" else 0x3498DB,
                "fields": [
                    {"name": "🏢 Компания", "value": obj.company_name, "inline": False},
                    {"name": "👤 Контактно лице", "value": obj.contact_person_names, "inline": True},
                    {"name": "📧 Имейл", "value": obj.email, "inline": True},
                    {"name": "📞 Телефон", "value": obj.phone or "—", "inline": True},
                    {"name": "💎 Ниво", "value": obj.tier.capitalize() if obj.tier else "Не е посочено", "inline": True},
                    {"name": "📝 Описание", "value": obj.description or "—", "inline": False},
                ],
                "footer": {
                    "text": f"📅 Изпратено на {obj.created_at.strftime('%d.%m.%Y %H:%M')}"
                }
            }

            try:
                requests.post(DISCORD_WEBHOOK_URL, json={"embeds": [embed]})
            except Exception as e:
                print(f"[Discord Error] {e}")

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
