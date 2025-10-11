from rest_framework import generics, permissions
from .models import Sponsor
from .serializers import SponsorSerializer

class SponsorListCreateView(generics.ListCreateAPIView):
  queryset = Sponsor.objects.all()
  serializer_class = SponsorSerializer

  def get_permissions(self):
      if self.request.method == "GET":
          return [permissions.AllowAny()]
      return [permissions.IsAuthenticated()]


class SponsorDetailView(generics.RetrieveUpdateDestroyAPIView):
  queryset = Sponsor.objects.all()
  serializer_class = SponsorSerializer

  def get_permissions(self):
      if self.request.method == "GET":
          return [permissions.AllowAny()]
      return [permissions.IsAuthenticated()]
