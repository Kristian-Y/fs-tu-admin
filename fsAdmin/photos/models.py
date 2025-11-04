from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete
from cloudinary.models import CloudinaryField
import cloudinary.uploader

class Album(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Photo(models.Model):
    album = models.ForeignKey(Album, related_name='photos', on_delete=models.CASCADE)
    image = CloudinaryField('image')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.image)
    
@receiver(post_delete, sender=Photo)
def delete_image_from_cloudinary(sender, instance, **kwargs):
    if instance.image:
        try:
            cloudinary.uploader.destroy(instance.image.public_id)
            print(f"🗑️ Изтрита снимка от Cloudinary: {instance.image.public_id}")
        except Exception as e:
            print(f"⚠️ Грешка при изтриване от Cloudinary: {e}")