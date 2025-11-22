from rest_framework import generics, permissions
from .models import SponsorApplication, MemberApplication, ContactMessage
from .serializers import SponsorApplicationSerializer, MemberApplicationSerializer, ContactMessageSerializer
from django.conf import settings
import requests

DISCORD_WEBHOOK_SUPP_URL = getattr(settings, "DISCORD_WEBHOOK_SUPP_URL", None)
DISCORD_WEBHOOK_JOIN_URL = getattr(settings, "DISCORD_WEBHOOK_JOIN_URL", None)
DISCORD_WEBHOOK_CONTACT_URL = getattr(settings, "DISCORD_WEBHOOK_CONTACT_URL", None)


class SponsorApplicationCreateView(generics.ListCreateAPIView):
    queryset = SponsorApplication.objects.all().order_by('-created_at')
    serializer_class = SponsorApplicationSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        obj = serializer.save()
        
        if DISCORD_WEBHOOK_SUPP_URL:
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
                requests.post(DISCORD_WEBHOOK_SUPP_URL, json={"embeds": [embed]})
            except Exception as e:
                print(f"[Discord Error] {e}")

class MemberApplicationCreateView(generics.ListCreateAPIView):
    queryset = MemberApplication.objects.all().order_by('-created_at')
    serializer_class = MemberApplicationSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        obj = serializer.save()

        if DISCORD_WEBHOOK_JOIN_URL:
            embed = {
                "title": "🆕 Нова кандидатура за член!",
                "color": 0x3498DB,
                "fields": [
                    {"name": "👤 Име", "value": f"{obj.first_name} {obj.last_name}", "inline": False},
                    {"name": "📧 Имейл", "value": obj.email, "inline": True},
                    {"name": "📞 Телефон", "value": obj.phone or "—", "inline": True},

                    {"name": "🏛 Университет", "value": obj.university or "—", "inline": False},
                    {"name": "🎓 Специалност", "value": obj.major or "—", "inline": True},
                    {"name": "📅 Година на завършване", "value": obj.graduation or "—", "inline": True},

                    {"name": "📘 Курс", "value": obj.course or "—", "inline": True},
                    {"name": "🗓 Семестър", "value": obj.semester or "—", "inline": True},

                    {"name": "🛠 Умения", "value": obj.skills or "—", "inline": False},
                    {"name": "🔥 Мотивация", "value": obj.motivation or "—", "inline": False},

                    {"name": "🔗 Портфолио", "value": obj.portfolio_link or "—", "inline": False},
                ],
                "footer": {
                    "text": f"📅 Изпратено на {obj.created_at.strftime('%d.%m.%Y %H:%M')}"
                }
            }

            try:
                requests.post(DISCORD_WEBHOOK_JOIN_URL, json={"embeds": [embed]})
            except Exception as e:
                print(f"[Discord Error] {e}")

class ContactMessageCreateView(generics.ListCreateAPIView):
    queryset = ContactMessage.objects.all().order_by("-created_at")
    serializer_class = ContactMessageSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        obj = serializer.save()

        if DISCORD_WEBHOOK_CONTACT_URL:
            embed = {
                "title": "📩 Ново съобщение от контактната форма",
                "color": 0x7289DA,
                "fields": [
                    {"name": "👤 Име", "value": obj.name, "inline": False},
                    {"name": "📧 Имейл", "value": obj.email, "inline": True},
                    {"name": "📝 Тема", "value": obj.subject, "inline": True},
                    {"name": "💬 Съобщение", "value": obj.message, "inline": False},
                ],
                "footer": {
                    "text": f"📅 Изпратено на {obj.created_at.strftime('%d.%m.%Y %H:%M')}"
                }
            }

            try:
                requests.post(DISCORD_WEBHOOK_CONTACT_URL, json={"embeds": [embed]})
            except Exception as e:
                print(f"[Discord Error] {e}")