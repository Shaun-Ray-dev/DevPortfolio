from django.urls import path
from . import views

urlpatterns = [
    path('', views.stash_view, name='home'),  
    path('stash/', views.stash_view, name='stash'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
]


