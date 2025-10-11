from django.db import models

# Create your models here.
class Sponsor(models.Model):
  name = models.CharField(max_length=100)
  logo = models.ImageField(upload_to="sponsor_logos/")
  link = models.URLField(blank=True)

  def __str__(self):
    return f"{self.name}"