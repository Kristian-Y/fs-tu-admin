from django.urls import path
from .views import SponsorApplicationCreateView, MemberApplicationCreateView, ContactMessageCreateView

urlpatterns = [
    path('sponsor-applications/', SponsorApplicationCreateView.as_view(), name='sponsor-applications'),
    path('join-applications/', MemberApplicationCreateView.as_view(), name='sponsor-applications'),
    path("contact/", ContactMessageCreateView.as_view(), name="contact"),
]
