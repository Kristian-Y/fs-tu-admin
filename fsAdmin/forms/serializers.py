from rest_framework import serializers
from .models import SponsorApplication

class SponsorApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SponsorApplication
        fields = '__all__'
