from django.urls import path
from .views import SponsorListCreateView, SponsorDetailView


urlpatterns = [
    path('', SponsorListCreateView.as_view(), name='sponsor_list_create'),
    path('<int:pk>/', SponsorDetailView.as_view(), name='sponsor_detail'),
] 
