from rest_framework import generics, permissions
from .models import Year, TeamPhoto
from .serializers import YearSerializer, TeamPhotoSerializer

# ---------- TeamPhoto ----------
class TeamPhotoListCreateView(generics.ListCreateAPIView):
    queryset = TeamPhoto.objects.all()
    serializer_class = TeamPhotoSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

class TeamPhotoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TeamPhoto.objects.all()
    serializer_class = TeamPhotoSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

# ---------- Year ----------
class YearListCreateView(generics.ListCreateAPIView):
    queryset = Year.objects.all().order_by('-year')  # сортиране по година
    serializer_class = YearSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

class YearDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Year.objects.all()
    serializer_class = YearSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
    

class YearPhotosListView(generics.ListAPIView):
    queryset = Year.objects.all().order_by('-year')  # сортиране по година
    serializer_class = YearSerializer
    permission_classes = [permissions.AllowAny]  # GET е публичен