from django.db import models

# Create your models here.

class Year(models.Model):
  year = models.IntegerField(unique=True)

  def __str__(self):
    return f"{self.year}"

class TeamPhoto(models.Model):
  year = models.ForeignKey(Year, on_delete=models.CASCADE, related_name='photos')
  image = models.ImageField(upload_to="team_photos/")

  def __str__(self):
    return f"Photo from season {self.year.year}"