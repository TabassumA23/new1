"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin, auth
from django.urls import include, path
from django.http import HttpResponse
from . import views

from .views import login_user, logout_user, signup_user, reviews_api, review_api, restaurants_api, restaurant_api, users_api, user_api, friendship_api, friendships_api, chosens_api, chosen_api, update_password, update_username, chosenCuisines_api, chosenCuisine_api, cuisines_api, cuisine_api, reservation_api, reservations_api, allergy_api, allergys_api, recommend_restaurants, chosenAllergys_api, chosenAllergy_api, wishlist_api, wishlists_api,wishlist_items_api, wishlistItems_api,wishlistItem_api, share_wishlist, shared_wishlists

# Listing route URLs to views.
urlpatterns = [
    path('', login_user, name='user login'),
    path('login/', login_user, name='user login'),
    path('signup/', signup_user, name='user signup'),
    path('updatePass/', update_password, name='update password'),
    path('updateUser/', update_username, name='update user'),
    path('logout/', logout_user, name='user logout'),
    path('restaurants/', restaurants_api, name='restaurants api'),
    path('restaurant/<int:restaurant_id>/', restaurant_api, name='restaurant api'),
    path('reservations/', reservations_api, name='reservations api'),
    path('reservation/<int:reservation_id>/', reservation_api, name='reservation api'),
    path('reviews/', reviews_api, name='reviews api'),
    path('review/<int:review_id>/', review_api, name='review api'),
    path('cuisines/', cuisines_api, name='cuisines api'),
    path('cuisine/<int:cuisine_id>/', cuisine_api, name='cuisine api'),
    path('users/', users_api, name='users api'),
    path('user/<int:user_id>/', user_api, name='user api'),
    path('chosenCuisines/', chosenCuisines_api, name='chosenCuisines api'),
    path('chosenCuisine/<int:chosenCuisine_id>/', chosenCuisine_api, name='chosenCuisine api'),

    path('chosenAllergys/', chosenAllergys_api, name='chosenAllergys api'),
    path('chosenAllergy/<int:chosenAllergy_id>/', chosenAllergy_api, name='chosenAllergy api'),

    path('chosens/', chosens_api, name='chosens api'),
    path('chosen/<int:chosen_id>/', chosen_api, name='chosen api'),
    path('friendships/', friendships_api, name='friendships api'),
    path('friendship/<int:friendship_id>/', friendship_api, name='friendship api'),
    path('allergys/', allergys_api, name='allergys api'),
    path('allergy/<int:allergy_id>/', allergy_api, name='allergy api'),

    path('recommend_restaurants/', recommend_restaurants, name='recommend restaurants'),

    # path('wishlists/', views.wishlist_list_create, name='wishlist_list_create'),
    # path('wishlist/<int:wishlist_id>/share/', views.wishlist_share, name='wishlist_share'),
    path('wishlistItems/', wishlistItems_api, name='wishlistItems api'),
    path('wishlistItem/<int:wishlistItem_id>/', wishlistItem_api, name='wishlistItem api'),
    
    path("share_wishlist/<int:wishlist_id>/", views.share_wishlist),
    path("shared_wishlists/<int:user_id>/", views.get_shared_wishlists),



    path('wishlists/', wishlists_api, name='wishlists api'),
    path('wishlist/<int:wishlist_id>/', wishlist_api, name='wishlist api'),
    path('wishlist/<int:wishlist_id>/items/', wishlist_items_api),

    
    
]