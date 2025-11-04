from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db import transaction
from .models import Sponsor
import cloudinary.uploader

class SponsorListCreateView(generics.ListCreateAPIView):
    queryset = Sponsor.objects.all().order_by('-id')

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def list(self, request, *args, **kwargs):
        """Връща списък с всички спонсори + Cloudinary URL."""
        sponsors = self.get_queryset()
        data = [
            {
                "id": s.id,
                "name": s.name,
                "type": s.type,
                "link": s.link,
                "logo": s.logo_url,  # директен линк
            }
            for s in sponsors
        ]
        return Response(data)

    def create(self, request, *args, **kwargs):
        """Създава нов спонсор (логото автоматично се качва в Cloudinary)."""
        name = request.data.get("name")
        s_type = request.data.get("type", "bronze")
        link = request.data.get("link", "")
        logo = request.FILES.get("logo")

        if not name or not logo:
            return Response({"error": "Missing name or logo."}, status=400)

        sponsor = Sponsor.objects.create(name=name, type=s_type, link=link, logo=logo)
        return Response({
            "id": sponsor.id,
            "name": sponsor.name,
            "type": sponsor.type,
            "link": sponsor.link,
            "logo": sponsor.logo_url,
        }, status=201)


class SponsorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sponsor.objects.all()

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def retrieve(self, request, *args, **kwargs):
        sponsor = self.get_object()
        return Response({
            "id": sponsor.id,
            "name": sponsor.name,
            "type": sponsor.type,
            "link": sponsor.link,
            "logo": sponsor.logo_url,
        })

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        sponsor = self.get_object()
        logo_public_id = getattr(sponsor.logo, "public_id", None)
        self.perform_destroy(sponsor)

        if logo_public_id:
            try:
                cloudinary.uploader.destroy(logo_public_id)
                print(f"🗑️ Изтрито лого от Cloudinary: {logo_public_id}")
            except Exception as e:
                print(f"⚠️ Cloudinary delete error: {e}")

        return Response(status=status.HTTP_204_NO_CONTENT)
