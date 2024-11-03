from django.db import models
from Adminapp.models import ProductDB
# Create your models here.

class ContactDB(models.Model):
    Name = models.CharField(max_length=50,null=True,blank=True)
    Email = models.EmailField(max_length=50, null=True, blank=True)
    Subject = models.CharField(max_length=50, null=True, blank=True)
    Message = models.TextField(max_length=500, null=True, blank=True)


class RegisterDB(models.Model):
    Username = models.CharField(max_length=50,null=True,blank=True)
    Email = models.EmailField(max_length=50,null=True,blank=True)
    Password1 = models.CharField(max_length=50,null=True,blank=True)
    Password2 = models.CharField(max_length=50,null=True,blank=True)
    Image = models.ImageField(upload_to="Register Images", null=True, blank=True)


class CartDB(models.Model):
    User_Name = models.CharField(max_length=50,null=True,blank=True)
    Product_Name = models.CharField(max_length=50,null=True,blank=True)
    Quantity = models.IntegerField(null=True,blank=True)
    Price = models.IntegerField(null=True,blank=True)
    Total_Price = models.IntegerField(null=True,blank=True)
    Image = models.URLField(max_length=200, null=True, blank=True)


class WishlistDB(models.Model):
    User_Name = models.CharField(max_length=50,null=True,blank=True)
    Image = models.ImageField(upload_to="Wishlist Images", null=True, blank=True)
    Product_Name = models.CharField(max_length=50,null=True,blank=True)
    Price = models.IntegerField(null=True,blank=True)


class OrderDB(models.Model):
    Name = models.CharField(max_length=50,null=True,blank=True)
    Email = models.EmailField(max_length=50,null=True,blank=True)
    Phone = models.IntegerField(null=True,blank=True)
    Country = models.CharField(max_length=50,null=True,blank=True)
    State = models.CharField(max_length=50,null=True,blank=True)
    Pin = models.IntegerField(null=True,blank=True)
    Address = models.CharField(max_length=50,null=True,blank=True)
    Total_Price = models.IntegerField(null=True,blank=True)


class Review(models.Model):
    product = models.ForeignKey(ProductDB, on_delete=models.CASCADE, related_name="reviews")
    user_name = models.CharField(max_length=50, null=True, blank=True)  # Or link to user model if you have one
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)  # Rating from 1 to 5
    comment = models.TextField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_name} - {self.product.Product_Name} ({self.rating} stars)"