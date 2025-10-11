from rest_framework import serializers
from .models import Sponsor

class SponsorSerializer(serializers.ModelSerializer):
  class Meta:
    model = Sponsor
    fields = ['id', 'name', 'logo', 'link', 'year']
