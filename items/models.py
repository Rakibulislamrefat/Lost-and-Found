from django.db import models
from django.contrib.auth.models import User


class Item(models.Model):
    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('documents', 'Documents'),
        ('clothing', 'Clothing'),
        ('accessories', 'Accessories'),
        ('keys', 'Keys'),
        ('bags', 'Bags & Wallets'),
        ('others', 'Others'),
    ]

    TYPE_CHOICES = [
        ('lost', 'Lost'),
        ('found', 'Found'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('claimed', 'Claimed'),
        ('closed', 'Closed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items')
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='others')
    item_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    location = models.CharField(max_length=200)
    date_reported = models.DateField()
    image = models.ImageField(upload_to='items/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.get_item_type_display()}] {self.title}"

    @property
    def pending_claims_count(self):
        return self.claims.filter(status='pending').count()


class ClaimRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='claims')
    claimant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='claims')
    message = models.TextField(help_text='Describe why you believe this item belongs to you')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Claim by {self.claimant.username} on {self.item.title}"
