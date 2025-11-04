from django.db import models

class SponsorApplication(models.Model):
    TIER_CHOICES = [
        ('gold', 'Gold'),
        ('silver', 'Silver'),
        ('bronze', 'Bronze'),
        ('partner', 'Partner'),
        ('other', 'Other'),
    ]

    company_name = models.CharField(max_length=150)
    contact_person_names = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    description = models.TextField(blank=True)
    tier = models.CharField(max_length=20, choices=TIER_CHOICES, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company_name} ({self.contact_person_names})"
