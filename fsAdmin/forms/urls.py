from django.urls import path
from .views import SponsorApplicationCreateView

urlpatterns = [
    path('sponsor-applications/', SponsorApplicationCreateView.as_view(), name='sponsor-applications'),
]
