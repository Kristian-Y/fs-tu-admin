from rest_framework import serializers
from .models import Year, TeamPhoto

class TeamPhotoSerializer(serializers.ModelSerializer):
  class Meta:
    model = TeamPhoto
    fields = "__all__"

class YearSerializer(serializers.ModelSerializer):
  photos = TeamPhotoSerializer(many=True)

  class Meta:
    model = Year
    fields = "__all__"