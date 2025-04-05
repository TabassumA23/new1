import json
from django.conf import settings
from django.contrib.sessions.models import Session
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from .models import Chosen, Restaurant, User, Friendship, ChosenCuisine, Cuisine, Review
from .forms import LoginForm, SignUpForm, UpdatePassForm, UpdateUserForm

# Authenticate login before Vue SPA redirect
def login_user(request: HttpRequest) -> HttpResponse:
    """ Function to validate a potenital registered user. """
    if request.method == "POST":
        form = LoginForm(request.POST)
        # Clean values if valid and authenticate
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = auth.authenticate(username=username, password=password)
            # Rendering Vue SPA if user is found
            if user is not None:
                auth.login(request, user)
                # Saving user id in variable to add to redirect as query
                user_id=user.id
                return redirect(settings.LOGIN_REDIRECT_URL+'?u=%s' %user_id)
            else:
                # Show failed authentication
                return render(request, "api/auth/login.html", {"form": form, "message": 'Username or password invalid, please try again.'})
    else:
        form = LoginForm()
    return render(request, "api/auth/login.html", {"form": form})


# Authenticate signup and login before Vue SPA redirect
def signup_user(request: HttpRequest) -> HttpResponse:
    """ Function to register a new user. """
    if request.method == "POST":
        form = SignUpForm(request.POST)
        # Clean values if valid and authenticate
        if form.is_valid():
            first_name=form.cleaned_data["first_name"]
            last_name=form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email=form.cleaned_data["email"]
            date_of_birth=form.cleaned_data["date_of_birth"]
            password=form.cleaned_data["password"]
            user = auth.authenticate(username=username, password=password)
            # Rendering Vue SPA if an existing user is not found
            if user is None:
                # Create a new user with input form details
                user = User.objects.create_user(username=username, email=email, password=password)
                user.first_name=first_name
                user.last_name=last_name
                user.date_of_birth=date_of_birth
                user.save()

                auth.login(request, user)
                user_id=user.id
                return redirect(settings.LOGIN_REDIRECT_URL+'?u=%s' %user_id)
            else:
                # Show failed user creation
                return render(request, "api/auth/signup.html", {"form": form, "message": 'User already exists with that username. Please try again.'})
    else:
        form = SignUpForm()
    return render(request, "api/auth/signup.html", {"form": form})
        
@login_required
# Logout user below
def logout_user(request: HttpRequest) -> HttpResponse:
    """ Function to logout a user. """
    auth.logout(request)
    return redirect(settings.LOGIN_URL)

# APIs for restaurant model below
def restaurants_api(request: HttpRequest) -> JsonResponse:
    """API endpoint for the Restaurant"""

    # POST method which is the create method
    if request.method == 'POST':
        # Create a new restaurant
        POST = json.loads(request.body)
        restaurant = Restaurant.objects.create(
            name=POST['name'],
            description=POST['description'],
        )
        return JsonResponse(restaurant.as_dict())

    # GET method which allows the user to view all hobbies
    return JsonResponse({
        'restaurants': [
            restaurant.as_dict()
            for restaurant in Restaurant.objects.all()
        ]
    })

def restaurant_api(request: HttpRequest, restaurant_id: int) -> JsonResponse:
    """API endpoint for a single restaurant"""
    try:
        restaurant = Restaurant.objects.get(id=restaurant_id)
    except Restaurant.DoesNotExist:
        return JsonResponse({"error": "Restaurant not found."}, status=404)

    # PUT method to update restaurant
    if request.method == 'PUT':
        try:
            PUT = json.loads(request.body)
            restaurant.name = PUT.get("name", restaurant.name)
            restaurant.description = PUT.get("description", restaurant.description)
            restaurant.save()
            return JsonResponse(restaurant.as_dict())
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    # DELETE method to delete restaurant
    if request.method == 'DELETE':
        restaurant.delete()
        return JsonResponse({}, status=204)  # 204 No Content

    # GET restaurant data
    return JsonResponse(restaurant.as_dict())

# APIs for user model below
def users_api(request: HttpRequest) -> JsonResponse:
    """API endpoint for the Users"""

    if request.method == 'POST':
        try:
            POST = json.loads(request.body)
            required_fields = ['first_name', 'last_name', 'email', 'date_of_birth', 'password']
            missing_fields = [field for field in required_fields if field not in POST]
            if missing_fields:
                return JsonResponse({"error": f"Missing fields: {', '.join(missing_fields)}"}, status=400)

            chosen_restaurants = POST.get('chosen_restaurant', [])
            user = User.objects.create(
                first_name=POST['first_name'],
                last_name=POST['last_name'],
                email=POST['email'],
                date_of_birth=POST['date_of_birth'],
                password=POST['password'],
            )

            for chosen_restaurant_id in chosen_restaurants:
                chosen_restaurant = Restaurant.objects.get(id=chosen_restaurant_id)  # Ensure hobbies exist
                user.chosen_restaurant.add(chosen_restaurant)

            return JsonResponse(user.as_dict(), status=201)
        #restaurant not found when is retrived by id 
        except Restaurant.DoesNotExist:
            return JsonResponse({"error": "restaurant not found."}, status=400)
        #general error hendler 
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    # GET Method
    return JsonResponse({
        'users': [
            user.as_dict()
            for user in User.objects.all()
        ]
    })

def user_api(request: HttpRequest, user_id: int) -> JsonResponse:
    """API endpoint for a single user"""
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)

    # PUT method
    if request.method == 'PUT':
        try:
            PUT = json.loads(request.body)
            user.first_name = PUT.get("first_name", user.first_name)
            user.last_name = PUT.get("last_name", user.last_name)
            user.email = PUT.get("email", user.email)
            user.date_of_birth = PUT.get("date_of_birth", user.date_of_birth)
            user.password = PUT.get("password", user.password)

            user.save()
            return JsonResponse({"success": "User updated successfully."})
        except Restaurant.DoesNotExist:
            return JsonResponse({"error": "restaurant not found."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    # DELETE method
    if request.method == 'DELETE':
        user.delete()
        return JsonResponse({})

    # GET method
    return JsonResponse(user.as_dict())

# APIs for friendship model below
def friendships_api(request: HttpRequest) -> JsonResponse:
    """API endpoint for the Friendship"""

    # POST method which is the create method
    if request.method == 'POST':
        # Create a new friendship
        POST = json.loads(request.body)
        user = User.objects.get(id=POST.get("user_id"))
        friend = User.objects.get(id=POST.get("friend_id"))

        friendship = Friendship.objects.create(
            user = user,
            friend = friend,
            accepted = POST['accepted'],
        )
        return JsonResponse(friendship.as_dict())

    # GET method which allows the user to view all hobbies
    return JsonResponse({
        'friendships': [
            friendship.as_dict()
            for friendship in Friendship.objects.all()
        ]
    })

def friendship_api(request: HttpRequest, friendship_id: int) -> JsonResponse:
    """API endpoint for a single friendship"""
    try:
        friendship = Friendship.objects.get(id=friendship_id)
    except Friendship.DoesNotExist:
        return JsonResponse({"error": "Friendship not found."}, status=404)

    if request.method == 'PUT':
        # Ensure the user has permission to accept the friendship
        if request.user.id != friendship.user.id:
            return JsonResponse({"error": "Unauthorized to accept this friendship."}, status=403)

        friendship.accepted = True
        friendship.save()
        return JsonResponse({"friendship": friendship.as_dict()})

    elif request.method == 'DELETE':
        # Ensure the user has permission to delete the friendship
        if request.user.id != friendship.user.id:
            return JsonResponse({"error": "Unauthorized to delete this friendship."}, status=403)

        friendship.delete()
        return JsonResponse({}, status=204)  # 204 No Content

    return JsonResponse(friendship.as_dict())


# APIs for chosen model below
def chosens_api(request: HttpRequest) -> JsonResponse:
    """API endpoint for the Chosen"""

    # POST method which is the create method
    if request.method == 'POST':
        try:
            # Create a new restaurant
            POST = json.loads(request.body)
            user = User.objects.get(id=POST.get("user_id"))
            restaurant = Restaurant.objects.get(id=POST.get("restaurant_id"))
            chosen = Chosen.objects.create(
                user = user,
                restaurant = restaurant,

            )
            return JsonResponse(chosen.as_dict())
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Invalid user_id or restaurant_id'}, status=404)
        except IntegrityError:
            return JsonResponse({'error': 'Chosen creation failed due to integrity error'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON payload'}, status=400)

    # GET method which allows the user to view all hobbies
    return JsonResponse({
        'chosens': [
            chosen.as_dict()
            for chosen in Chosen.objects.all()
        ]
    })


def chosen_api(request: HttpRequest, chosen_id: int) -> JsonResponse:
    """API endpoint for a single chosen"""
    try:
        chosen = Chosen.objects.get(id=chosen_id)
    except chosen.DoesNotExist:
        return JsonResponse({"error": "Chosen not found."}, status=404)

    # PUT method to update chosen need to finish
    

    # DELETE method to delete chosen
    if request.method == 'DELETE':
        chosen.delete()
        return JsonResponse({}, status=204)  # 204 No Content

    # GET chosen data
    return JsonResponse(chosen.as_dict())



@login_required
def update_password(request: HttpRequest) -> HttpResponse:
    """ Function to validate a potenital registered user. """
    if request.method == "POST":
        form = UpdatePassForm(request.POST)  # Use a form specifically for password updates
        if form.is_valid():
            password = form.cleaned_data["password"]

            try:
                if not password:
                    return JsonResponse({"error": "Password is required."}, status=400)

                # Use the currently logged-in user to update the password
                user = request.user
                user.set_password(password)  # Hash and set the new password
                user.save() 
                return redirect(settings.LOGIN_URL)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)

        # Return form errors if invalid
        return render(request, "api/auth/updatePass.html", {"form": form, "errors": form.errors})

    # For GET requests, display the form
    else:
        form = UpdatePassForm()
    return render(request, "api/auth/updatePass.html", {"form": form})


@login_required
def update_username(request: HttpRequest) -> HttpResponse:
    """Function to update the username of the logged-in user."""
    if request.method == "POST":
        form = UpdateUserForm(request.POST)
        if form.is_valid():
            new_username = form.cleaned_data["new_username"]

            try:
                # Ensure the new username is not already taken
                if User.objects.filter(username=new_username).exists():
                    return render(request, "api/auth/updateUsername.html", {"form": form, "message": "username exists already"})
                    return redirect(settings.LOGIN_URL)

                # Update the username
                user = request.user
                user.username = new_username
                user.save()

                return redirect(settings.LOGIN_URL)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)

        # Render form with errors if invalid
        return render(request, "api/auth/updateUsername.html", {"form": form, "errors": form.errors})

    # For GET requests, display the form
    else:
        form = UpdateUserForm()
        return render(request, "api/auth/updateUsername.html", {"form": form})
    
# APIs for cuisine model below
def cuisines_api(request: HttpRequest) -> JsonResponse:
    """API endpoint for the Cuisine"""

    # POST method which is the create method
    if request.method == 'POST':
        # Create a new cuisine
        POST = json.loads(request.body)
        cuisine = Cuisine.objects.create(
            name=POST['name'],
            description=POST['description'],
        )
        return JsonResponse(cuisine.as_dict())

    # GET method which allows the user to view all hobbies
    return JsonResponse({
        'cuisines': [
            cuisine.as_dict()
            for cuisine in Cuisine.objects.all()
        ]
    })

def cuisine_api(request: HttpRequest, cuisine_id: int) -> JsonResponse:
    """API endpoint for a single cuisine"""
    try:
        cuisine = Cuisine.objects.get(id=cuisine_id)
    except Cuisine.DoesNotExist:
        return JsonResponse({"error": "cuisine not found."}, status=404)

    # PUT method to update cuisine
    if request.method == 'PUT':
        try:
            PUT = json.loads(request.body)
            cuisine.name = PUT.get("name", cuisine.name)
            cuisine.description = PUT.get("description", cuisine.description)
            cuisine.save()
            return JsonResponse(cuisine.as_dict())
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    # DELETE method to delete cuisine
    if request.method == 'DELETE':
        cuisine.delete()
        return JsonResponse({}, status=204)  # 204 No Content

    # GET cuisine data
    return JsonResponse(cuisine.as_dict())

# APIs for chosenCuisine model below
def chosenCuisines_api(request: HttpRequest) -> JsonResponse:
    """API endpoint for the chosenCuisine"""

    # POST method which is the create method
    if request.method == 'POST':
        try:
            # Create a new restaurant
            POST = json.loads(request.body)
            user = User.objects.get(id=POST.get("user_id"))
            cuisine = Cuisine.objects.get(id=POST.get("cuisine_id"))
            chosenCuisine = ChosenCuisine.objects.create(
                user = user,
                cuisine = cuisine,

            )
            return JsonResponse(chosenCuisine.as_dict())
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Invalid user_id or restaurant_id'}, status=404)
        except IntegrityError:
            return JsonResponse({'error': 'chosenCuisine creation failed due to integrity error'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON payload'}, status=400)

    # GET method which allows the user to view all hobbies
    return JsonResponse({
        'chosenCuisines': [
            chosenCuisine.as_dict()
            for chosenCuisine in ChosenCuisine.objects.all()
        ]
    })


def chosenCuisine_api(request: HttpRequest,  chosenCuisine_id: int) -> JsonResponse:
    """API endpoint for a single chosenCuisine"""
    try:
        chosenCuisine = ChosenCuisine.objects.get(id=chosenCuisine_id)
    except chosenCuisine.DoesNotExist:
        return JsonResponse({"error": "chosenCuisine not found."}, status=404)

    # PUT method to update chosenCuisine need to finish
    

    # DELETE method to delete chosenCuisine
    if request.method == 'DELETE':
        chosenCuisine.delete()
        return JsonResponse({}, status=204)  # 204 No Content

    # GET chosenCuisine data
    return JsonResponse(chosenCuisine.as_dict())

# APIs for restaurant model below
def reviews_api(request: HttpRequest) -> JsonResponse:
    """API endpoint for the Review"""

    if request.method == 'POST':
        try:
            POST = json.loads(request.body)
            user_id = POST['user_id']
            # Use 'description' instead of 'review' to match the model
            review = Review.objects.create(
                name=POST['name'],
                description=POST['description'],  # Use 'description' field here
                user=User.objects.get(id=user_id),  # Use the user_id from the request
            )
            return JsonResponse(review.as_dict())
        except KeyError as e:
            return JsonResponse({'error': f'Missing required field: {str(e)}'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

    # If GET method is used, return all reviews with user details
    reviews = Review.objects.all()
    reviews_data = []
    for review in reviews:
        reviews_data.append({
            'id': review.id,
            'name': review.name,
            'description': review.description,  
            'date': review.date,
            'user': {
                'first_name': review.user.first_name,
                'last_name': review.user.last_name,
            },
        })
    return JsonResponse({'reviews': reviews_data})

def review_api(request: HttpRequest, review_id: int) -> JsonResponse:
    """API endpoint for a single review"""
    try:
        review = Review.objects.get(id=review_id)
    except Review.DoesNotExist:
        return JsonResponse({"error": "Review not found."}, status=404)

    # PUT method to update restaurant
    if request.method == 'PUT':
        try:
            PUT = json.loads(request.body)
            review.name = PUT.get("name", review.name)
            review.description = PUT.get("description", review.description)
            review.save()
            return JsonResponse(review.as_dict())
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    # DELETE method to delete restaurant
    if request.method == 'DELETE':
        review.delete()
        return JsonResponse({}, status=204)  # 204 No Content

    # GET restaurant data
    return JsonResponse(review.as_dict())
