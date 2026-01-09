from django.shortcuts import render
from .models import CollectionItem, WishlistItem
from .utils import get_item_val  
from django.utils import timezone

def stash_view(request):
    items = CollectionItem.objects.all()

    for item in items:
        current_val = get_item_val(item.item)
        if current_val is not None and current_val != item.market_value:
            item.market_value = current_val
            item.last_checked = timezone.now()
            item.save()

    return render(request, "stash/stash.html", {"items": items})

def wishlist_view(request):
    items = WishlistItem.objects.all()
    return render(request, "stash/wishlist.html", {"items": items})

