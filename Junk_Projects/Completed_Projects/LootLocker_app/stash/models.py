from django.db import models



class CollectionItem(models.Model):
    item = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    subcategory = models.CharField(max_length=255, null=True, blank=True)
    edition = models.CharField(max_length=255, null=True, blank=True)
    brand = models.CharField(max_length=255, null=True, blank=True)
    year = models.CharField(max_length=10, null=True, blank=True)
    condition = models.CharField(max_length=255, null=True, blank=True)
    market_value = models.FloatField(null=True, blank=True)
    last_checked = models.DateTimeField(auto_now=True)
    
class WishlistItem(models.Model):
    item = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    subcategory = models.CharField(max_length=255, null=True, blank=True)
    edition = models.CharField(max_length=255, null=True, blank=True)
    brand = models.CharField(max_length=255, null=True, blank=True)
    year = models.CharField(max_length=10, null=True, blank=True)
    condition = models.CharField(max_length=255, null=True, blank=True)
    desired_price = models.FloatField(null=True, blank=True)
    last_checked = models.DateTimeField(auto_now=True)

