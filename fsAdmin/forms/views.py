from rest_framework import generics, permissions
from .models import SponsorApplication
from .serializers import SponsorApplicationSerializer

class SponsorApplicationCreateView(generics.ListCreateAPIView):
    queryset = SponsorApplication.objects.all().order_by('-created_at')
    serializer_class = SponsorApplicationSerializer
    permission_classes = [permissions.AllowAny]
