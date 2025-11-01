from django.db import models

# Create your models here.
class Sponsor(models.Model):
  TYPES = [
    ('gold', 'Gold'),
    ('silver', 'Silver'),
    ('bronze', 'Bronze'),
    ('partner', 'Partner'),
  ]
  name = models.CharField(max_length=100)
  type = models.CharField(choices=TYPES, max_length=10, default='bronze')
  logo = models.ImageField(upload_to="sponsor_logos/")
  link = models.URLField(blank=True)

  def __str__(self):
    return f"{self.name}"