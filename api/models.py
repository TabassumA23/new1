from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import logging

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a file handler and a stream handler
file_handler = logging.FileHandler('app.log')
stream_handler = logging.StreamHandler()

# Create a formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)


# Create your models here.


class PageView(models.Model):
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"Page view count: {self.count}"


class Restaurant(models.Model):
    '''
    Class for the restaurant
    '''
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=100)
    
    def __str__(self):
        return self.name
    
    '''
    Dictionary
    '''
    def as_dict(self):
        return {
            'id': self.id,
            # Obtains URL pattern for individual restaurant
            'api': reverse('restaurant api', args=[self.id]),
            'name': self.name,
            'description': self.description,
        }
    
class Cuisine(models.Model):
    '''
    Class for the cusine
    '''
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=100)
    
    def __str__(self):
        return self.name
    
    '''
    Dictionary
    '''
    def as_dict(self):
        return {
            'id': self.id,
            # Obtains URL pattern for individual cuisine
            'api': reverse('cuisine api', args=[self.id]),
            'name': self.name,
            'description': self.description,
        }
    

class User(AbstractUser):
    '''
    Class containing the custom user model which inherits the abstract user model from django making use of 
    authentication framework    
    '''
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(default='2000-01-01')
    password = models.CharField(max_length=100)
    chosen_restaurant = models.ManyToManyField(Restaurant, through='Chosen')
    chosen_cuisine = models.ManyToManyField(Cuisine, through='ChosenCuisine')
    # Many-to-many fields to store multiple IDs
    friends = models.ManyToManyField('self', through='Friendship', symmetrical=False, related_name="friends_with+")

    def __str__(self):
        return f"{self.first_name, self.last_name}"
    
    '''
    Dictionary
    '''
    def as_dict(self):
        # Gets the list of actual cuisine objects a user has added. 
        user_cuisines = list(Cuisine.objects.values().filter(name="Reading"))
        return {  
            'id': self.id,  
            # Obtains URL pattern for individual user
            'api': reverse('user api', args=[self.id]),
            'username' : self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'date_of_birth': self.date_of_birth,
            'password': self.password,
        }
    

    
class Chosen(models.Model):
     """
    This class is the Chosen Model which is a through model 
    which creates a many to many relationship between user and restaurant
    """
     user = models.ForeignKey('User', on_delete=models.CASCADE)
     restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE)
     name= models.CharField(max_length=100, default="chosen")
     def as_dict(self):
        return{
            'id': self.id,
            'api': reverse('chosen api', args=[self.id]),
            'user': self.user.id,
            'restaurant': self.restaurant.id,
            'name': self.restaurant.name,
        }
class ChosenCuisine(models.Model):
     """
    This class is the ChosenCuisine Model which is a through model 
    which creates a many to many relationship between user and cuisine
    """
     user = models.ForeignKey('User', on_delete=models.CASCADE)
     cuisine = models.ForeignKey('Cuisine', on_delete=models.CASCADE)
     name= models.CharField(max_length=100, default="chosenCuisine")
     def as_dict(self):
        return{
            'id': self.id,
            'api': reverse('chosen api', args=[self.id]),
            'user': self.user.id,
            'cuisine': self.cuisine.id,
            'name': self.cuisine.name,
        }

class Friendship(models.Model):
    """
    This class is the Friendship Model which is a through model 
    which creates a many to many relationship between user and friend
    """
    user = models.ForeignKey('User', related_name="from_user", on_delete=models.CASCADE)
    friend = models.ForeignKey('User', related_name="to_user", on_delete=models.CASCADE)
    username = models.CharField(max_length=100, default="username")
    accepted = models.BooleanField(default=False)

    def as_dict(self):
        return{
            'id': self.id,
            'api': reverse('friendship api', args=[self.id]),
            'user': self.user.id,
            'friend': self.friend.id,
            'username': self.friend.username,
            'accepted': self.accepted,
        }

class Review(models.Model):
    '''
    Class for the review
    '''
    name = models.CharField(max_length=255)  # Add a name field
    description = models.TextField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Foreign key to User model
    date = models.DateTimeField(default=timezone.now)  
    
    def __str__(self):
        return self.name
    
    '''
    Dictionary
    '''
    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'date': self.date,
            'user': {
                'first_name': self.user.first_name,
                'last_name': self.user.last_name,
                'id': self.user.id,
            }
        }
    