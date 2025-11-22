from rest_framework import serializers
from .models import SponsorApplication, MemberApplication, ContactMessage

class SponsorApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SponsorApplication
        fields = '__all__'


class MemberApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberApplication
        fields = '__all__'

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = "__all__"