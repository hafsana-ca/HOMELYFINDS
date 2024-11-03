from django.db import models
from django.db import models
from django.utils import timezone

# Create your models here.

class CategoryDB(models.Model):
    Name = models.CharField(max_length=50,null=True,blank=True)
    Description = models.CharField(max_length=300, null=True, blank=True)
    Image = models.ImageField(upload_to="Category Images", null=True, blank=True)


class ProductDB(models.Model):
    Category_Name = models.CharField(max_length=50,null=True,blank=True)
    Product_Name = models.CharField(max_length=50, null=True, blank=True)
    Brand_Name = models.CharField(max_length=50, null=True, blank=True)
    Price = models.CharField(max_length=50, null=True, blank=True)
    Weight = models.CharField(max_length=50, null=True, blank=True)
    Description = models.CharField(max_length=300, null=True, blank=True)
    Image1 = models.ImageField(upload_to="Product Images", null=True, blank=True)
    Image2 = models.ImageField(upload_to="Product Images", null=True, blank=True)
    Image3 = models.ImageField(upload_to="Product Images", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Add this field to track when the product is added
    # Add a status field to mark the product as available or coming soon
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('coming_soon', 'Coming Soon'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    is_deal_of_the_week = models.BooleanField(default=False)  # New field to mark the product as a deal


class HotDealDB(models.Model):
    title = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    products = models.ManyToManyField(ProductDB)  # Many-to-Many relationship with Product

    def has_ended(self):
        return timezone.now() > self.end_date  # Check if the deal has ended

    def __str__(self):
        return self.title


