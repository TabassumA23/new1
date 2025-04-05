from django.contrib import admin

# Register your models here.

from .models import User, Restaurant, Cuisine, Review

'''Register the friendship through model to the admin panel'''

class FriendshipInline(admin.TabularInline):
    model = User.friends.through
    fk_name = 'user'

'''Register the friendship through model to the admin panel'''

class ChosenInline(admin.TabularInline):
    model = User.chosen_restaurant.through
    fk_name = 'user'

class ChosenCuisineInline(admin.TabularInline):
    model = User.chosen_cuisine.through
    fk_name = 'user'


'''Register the user model to the admin panel'''
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = (ChosenInline, FriendshipInline, ChosenCuisineInline)


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    '''Register the restaurant model to the admin panel'''
    list_display = ('name', 'description')

@admin.register(Cuisine)
class CuisineAdmin(admin.ModelAdmin):
    '''Register the cuisine model to the admin panel'''
    list_display = ('name', 'description')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    '''Register the cuisine model to the admin panel'''
    list_display = ('name', 'description', 'user')


