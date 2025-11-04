from django.db import models
from cloudinary.models import CloudinaryField
from django.db.models.signals import post_delete
from django.dispatch import receiver
import cloudinary.uploader

class Sponsor(models.Model):
    TYPES = [
        ('gold', 'Gold'),
        ('silver', 'Silver'),
        ('bronze', 'Bronze'),
        ('partner', 'Partner'),
    ]

    name = models.CharField(max_length=100)
    type = models.CharField(choices=TYPES, max_length=10, default='bronze')
    logo = CloudinaryField('image', folder="sponsor_logos/")
    link = models.URLField(blank=True)

    def __str__(self):
        return self.name

    @property
    def logo_url(self):
        """Връща директния Cloudinary URL за React фронтенда."""
        return self.logo.url if self.logo else None


@receiver(post_delete, sender=Sponsor)
def delete_logo_from_cloudinary(sender, instance, **kwargs):
    if instance.logo:
        try:
            cloudinary.uploader.destroy(instance.logo.public_id)
            print(f"🗑️ Изтрито лого от Cloudinary: {instance.logo.public_id}")
        except Exception as e:
            print(f"⚠️ Грешка при изтриване от Cloudinary: {e}")
