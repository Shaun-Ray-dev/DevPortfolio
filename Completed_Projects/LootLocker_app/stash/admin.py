from django.contrib import admin




from django.contrib import admin
from .models import CollectionItem, WishlistItem

admin.site.register(CollectionItem)
admin.site.register(WishlistItem)

