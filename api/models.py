from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser, User
from django.utils import timezone
import logging
from django.core.validators import MinValueValidator
from django.conf import settings


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
    rating = models.IntegerField(default=0)
    seats_available = models.IntegerField(default=0)
    location = models.TextField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
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
            'rating': self.rating,
            'seats_available': self.seats_available,
            'location' : self.location,
            'user': {
                'first_name': self.user.first_name,
                'last_name': self.user.last_name,
                'id': self.user.id,
            }
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
    chosen_restaurant = models.ManyToManyField(Restaurant, through='Chosen', related_name="related_rest+")
    chosen_cuisine = models.ManyToManyField(Cuisine, through='ChosenCuisine')
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

class Reservation(models.Model):
    '''
    Class for the Reservation
    '''
    # Define status choices
    PENDING = 0
    CONFIRMED = 1
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (CONFIRMED, 'Confirmed'),
    ]
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)  # Link to Restaurant model
    reservation_time = models.DateTimeField()
    number_of_people = models.IntegerField(default=0,validators=[MinValueValidator(0)])
    status = models.IntegerField(choices=STATUS_CHOICES, default=PENDING)
    special_requests = models.TextField(max_length=200)
    
    def __str__(self):
        return f"Reservation at {self.restaurant.name} for {self.number_of_people} people"
    
    '''
    Dictionary
    '''
    def as_dict(self):
        return {
            'id': self.id,
            # Obtains URL pattern for individual restaurant
            'api': reverse('reservation api', args=[self.id]),
            'restaurant': self.restaurant.name,
            'special_requests': self.special_requests,
            'number_of_people': self.number_of_people,
            'status': dict(self.STATUS_CHOICES).get(self.status),
            'reservation_time': self.reservation_time.strftime('%Y-%m-%d %H:%M:%S'),
        }

