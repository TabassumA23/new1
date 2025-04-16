<template>
  <div class="body">
    <div id="profile-box">
      <h2>Welcome {{ user.first_name }}</h2>

      <!-- Form to Add a New restaurant. -->
      <div id="create-restaurant">
        <h3>Want to add a new restaurant to this website?</h3>
        <h6>Double check spelling before submission!!</h6>

        <label for="name">Name of restaurant:</label><br />
        <input
          id="name"
          v-model="newRestaurant.name"
          type="text"
          required
          class="form-control"
        /><br />

        <label for="description">Brief restaurant Description:</label><br />
        <textarea
          id="description"
          v-model="newRestaurant.description"
          required
          class="form-control"
          rows="2"
          cols="50"
        ></textarea><br />

        <label for="rating">Rating:</label><br />
        <input
          id="rating"
          v-model="newRestaurant.rating"
          type="number"
          min="1"
          max="5"
          required
          class="form-control"
        /><br />

        <label for="seats_available">Seats Available:</label><br />
        <input
          id="seats_available"
          v-model="newRestaurant.seats_available"
          type="number"
          required
          class="form-control"
        /><br />

        <label for="location">Location:</label><br />
        <select
          id="location"
          v-model="newRestaurant.location"
          required
          class="form-control"
        >
          <option value="London">London</option>
          <option value="Manchester">Manchester</option>
          <option value="Leeds">Leeds</option>
          <option value="Liverpool">Liverpool</option>
          <option value="Sheffield">Sheffield</option>
          <option value="Bristol">Bristol</option>
          <option value="Nottingham">Nottingham</option>
        </select><br />

        <button type="submit" @click="createRestaurant">Save</button>
      </div>
    </div>

    <div class="restaurant-blog">
      <h2>My restaurants</h2>

    <div
        class="restaurant-item"
        
        v-for="(restaurant, index) in restaurants"
        :key="index"
        
    >
        <div class="restaurant-header">
          <h3>Name: {{ restaurant.name }}</h3>
          <p>
            <strong>By:</strong> {{ restaurant.user.id }} 
            <!-- | <strong>Date:</strong> {{ formatDate(restaurant.date) }} -->
          </p>
        </div>

        <div class="restaurant-content">
          <p>Description: {{ restaurant.description }}</p>
        </div>

        <div class="restaurant-content">
          <p>Rating: {{ restaurant.rating }}</p>
        </div>
        <div class="restaurant-content">
          <p>Seats:{{ restaurant.seats_available }}</p>
        </div>
        <div class="restaurant-content">
          <p>Location: {{ restaurant.location }}</p>
        </div>
        <div class="restaurant-actions" v-if="restaurant.user.id === user.id">
          <button @click="deleteRestaurant(restaurant.id)">Delete restaurant</button>
        </div>
      </div>
       <div
        class="restaurant-item"
        
        v-for="(reservation, index) in reservations"
        :key="index"
        
    >
        <div class="restaurant-header">
          <h3>Name: {{ reservation.name }}</h3>
          <p>
            <strong>By:</strong> {{ restaurant.user.id }} 
            <!-- | <strong>Date:</strong> {{ formatDate(restaurant.date) }} -->
          </p>
        </div>

        <div class="restaurant-content">
          <p>Description: {{ reservation.reservation_time }}</p>
        </div>

        <div class="restaurant-content">
          <p>Rating: {{ reservation.number_of_people }}</p>
        </div>
        <div class="restaurant-content">
          <p>Seats:{{ reservation.status }}</p>
        </div>
        <div class="restaurant-content">
          <p>Location: {{ reservation.special_requests }}</p>
        </div>
        <div class="restaurant-actions" v-if="restaurant.user.id === user.id">
          <button @click="deleteRestaurant(restaurant.id)">Delete restaurant</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
  import { defineComponent } from "vue";
  import { User, Restaurant, Friendship, Chosen,Cuisine, ChosenCuisine, Reservation} from "../types/index";
  import { useUserStore } from "../stores/user";
  import { useUsersStore } from "../stores/users";
  import { useRestaurantsStore } from "../stores/restaurants";
  import { useReservationsStore } from "../stores/reservations";
  import { useCuisinesStore } from "../stores/cuisines";
  import { useChosenStore } from "../stores/chosen";
  import { useChosensStore } from "../stores/chosens";
  import { useChosenCuisineStore } from "../stores/chosenCuisine";
  import { useChosenCuisinesStore } from "../stores/chosenCuisines";
  import { useFriendshipsStore } from "../stores/friendships";
  import VueCookies from 'vue-cookies';

  


  export default defineComponent({
      data() {
          return {
          
          newRestaurant: {
            name: "",
            description: "",
            rating: 0,
            seats_available: 0,
            location: "London",
          },
          chosenRestaurant: "",
          chosenReservation: "",
          
          chosenChosenCuisine: "",
          
          };
      },
      async mounted() {
          // Fetching csrf token using session cookie information on mount
          const sessionCookie = (document.cookie).split(';');
          let currentSessionid: string = ''
          console.log(sessionCookie)
          // Checking in UserStore with CSRF token
          for (let cookie of sessionCookie) {
              cookie = cookie.trim();
              console.log(cookie)
              if (cookie.startsWith("sessionid" + "=")) {
                  currentSessionid = cookie.substring("sessionid".length + 1);
              }
          }
          
          const previousSessionid : string | null = window.sessionStorage.getItem("session_id")
          // Loading values from user store if sessionId matches
          if(currentSessionid == previousSessionid){
              const userId = Number(window.sessionStorage.getItem("user_id"));
              try {
                  const userCookie = await this.userStore.fetchUserReturn(Number(window.sessionStorage.getItem("user_id")));
                  console.log("Fetched User:", userCookie);
              } catch (error) {
                  console.error("Error fetching user:", error);
              }
          
              console.log('checked sesh')
          }
          else{
              // Extracting user id from url query
              const params = new URLSearchParams(window.location.search);
              const userId: number = parseInt(params.get("u") || "0");
              console.log(userId)
              // Fetch user data using url query information on mount
              let user = await this.userStore.fetchUserReturn(userId);
              console.log(user)
              this.userStore.user = user;
              // Set session variable
              sessionStorage.setItem("user_id", userId.toString());
              
              // Fetching csrf token using session cookie information on mount
              const session_cookie = (document.cookie).split(';');
              console.log(session_cookie)

              //Update user state in UserStore with CSRF token
              for (let cookie of session_cookie) {
                  cookie = cookie.trim();
                  console.log(cookie)
                  if (cookie.startsWith("csrftoken" + "=")) {
                      this.userStore.setCsrfToken(cookie.substring("csrftoken".length + 1));

                      console.log(this.userStore.csrf)
                  }
                  //Update sessionStorage state in UserStore with CSRF token
                  console.log(cookie)
                  if (cookie.startsWith("sessionid" + "=")) {
                     // Set session variable
                     let sessionId = cookie.substring("csrftoken".length + 1);
                     sessionStorage.setItem("session_id", sessionId);
                  }
              }
          }
         
          // Fetching all restaurants from the backend
          let response = await fetch(`http://localhost:8000/restaurants/`);
          let restaurantData = await response.json();

          // Fetching all restaurants from the backend
          let resp = await fetch(`http://localhost:8000/reservations/`);
          let reservationData = await resp.json();

          // Update the state with the fetched restaurant data
          let madeReservations = reservationData.reservations as Reservation[];
          const reservationsStore = useReservationsStore();
          reservationsStore.saveReservations(madeReservations); 
          console.log(resp)
        

          // Update the state with the fetched restaurant data
          let madeRestaurants = restaurantData.restaurants as Restaurant[];
          const restaurantsStore = useRestaurantsStore();
          restaurantsStore.saveRestaurants(madeRestaurants); 
          console.log(response)

          // Fetching all cuisines from the backend
          let res = await fetch(`http://localhost:8000/cuisines/`);
          let cuisineData = await res.json();

          // Update the state with the fetched cuisine data
          let madeCuisines = cuisineData.cuisines as Cuisine[];
          const cuisinesStore = useCuisinesStore();
          cuisinesStore.saveCuisines(madeCuisines); 
          console.log(res)

          //fetch all the friendships
          let responseFriendship = await fetch("http://localhost:8000/friendships/");
          let dataFriendship = await responseFriendship.json();
          let friendships = dataFriendship.friendships as Friendship[];

          const storeFriendships = useFriendshipsStore();
          storeFriendships.saveFriendships(friendships);

          //fetch all the friendships
          let responseChosen = await fetch("http://localhost:8000/chosens/");
          let dataChosen = await responseChosen.json();
          let chosens = dataChosen.chosens as Chosen[];
  
          const storeChosens = useChosensStore();
          storeChosens.saveChosens(chosens);

          //fetch all the friendships
          let responseChosenCuisine = await fetch("http://localhost:8000/chosenCuisines/");
          let dataChosenCuisine = await responseChosenCuisine.json();
          let chosenCuisines = dataChosenCuisine.chosenCuisines as ChosenCuisine[];

          const storeChosenCuisines = useChosenCuisinesStore();
          storeChosenCuisines.saveChosenCuisines(chosenCuisines);
      },
      methods: {
          
          

         async createRestaurant() {
            const restaurantsStore = useRestaurantsStore();
            const userId = this.userStore.user.id;
            const newRestaurant = this.newRestaurant;
            const payload = {
                name: this.newRestaurant.name,
                description: this.newRestaurant.description,
                rating: this.newRestaurant.rating,
                seats_available: this.newRestaurant.seats_available,
                location: this.newRestaurant.location,
                user_id: userId
            };
            
            console.log(payload); 
            console.log(userId);  
            
            

            const restaurantResponse = await fetch('http://localhost:8000/restaurants/', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${VueCookies.get('access_token')}`,
                    'Content-Type': 'application/json',
                    'X-CSRFToken': VueCookies.get('csrftoken'),
                },
                credentials: 'include',
                body: JSON.stringify(payload),
            });

            const responseText = await restaurantResponse.text();  // Log raw response for debugging
            console.log(responseText);

            // Add the newly created review to the Pinia store
            // const data = await reviewResponse.json();
            // let createdReview = data.review;
            // reviewsStore.addReview(createdReview);
            window.location.reload();
            alert('restaurant added successfully!');
        },
        async deleteRestaurant(restaurantId: number) {
            // Check if the logged-in user is the one who wrote the review
            const restaurantToDelete = this.restaurants.find(restaurant => restaurant.id === restaurantId);
            if (!restaurantToDelete || restaurantToDelete.user.id !== this.user.id) {
                alert("You cannot delete this restaurant. Only the author can delete it.");
                return; // Prevent deletion
            }

            try {
                const response = await fetch(`http://localhost:8000/restaurant/${restaurantId}/`, {
                    method: 'DELETE',
                    headers: {
                        'Authorization': `Bearer ${VueCookies.get('access_token')}`,
                        'Content-Type': 'application/json',
                        'X-CSRFToken': VueCookies.get('csrftoken'),
                    },
                    credentials: 'include',
                });
                window.location.reload(); 
                if (response.ok) {
                    // Remove the deleted review from the list
                    this.restaurants = this.restaurants.filter(restaurant => restaurant.id !== restaurantId);
                    alert('Revrestaurantiew deleted successfully!');
                } else {
                    alert('Failed to delete the restaurant.');
                }
            } catch (error) {
                console.error('Error deleting restaurant:', error);
                alert('Failed to delete the revirestaurantew.');
            }
        },            
      },
      computed: {
          user() {
              const userStore = useUserStore;
              return this.userStore.user; // Bind to the fetched user data from Pinia store
          },
          restaurants(): Restaurant[]{
              const restaurantsStore = useRestaurantsStore;
              return this.restaurantsStore.restaurants; // Bind to the fetched cuisine data from Pinia store
          },
          reservations(): Reservation[]{
              const reservationsStore = useReservationsStore;
              return this.reservationsStore.reservations; // Bind to the fetched cuisine data from Pinia store
          },
    
      },
      setup() {
          const userStore = useUserStore();
          const restaurantsStore = useRestaurantsStore();
          const reservationsStore = useReservationsStore();
          const usersStore = useUsersStore();
          
          return { userStore , restaurantsStore, usersStore, reservationsStore };
      },
  });
  </script>


<style scoped>


<style scoped>
    /* General Body Styling */
    .body {
        font-family: Arial, Helvetica, sans-serif;
        display: grid;
        grid-template-columns: auto auto;
        grid-template-rows: 10% 30% 20% 30% 10%;
        gap: 1rem 0.25rem;
        background-color: #F0F8FF; /* Light blue background for the page */
    }

    /* Profile Box Styling */
    #profile-box {
        grid-column: 1;
        grid-row: 1/span 2;
        background-color: #4F97C6; /* Medium blue for profile box */
        padding: 2rem;
        border-radius: 8px;
    }

    /* Restaurant Section Styling */
    #restaurant {
        grid-column: 1;
        grid-row: 3;
        background-color: #B4DABA; /* Light blue for restaurant section */
        padding: 2rem;
        border-radius: 8px;
    }

    /* Create Restaurant Section Styling */
    #create-restaurant {
        grid-column: 1;
        grid-row: 4;
        padding-top: 0.5rem;
        background-color: #4F97C6; /* Medium blue background */
        border-radius: 8px;
    }

    #create-restaurant > h3 {
        text-align: center;
        background-color: #D9D9D9; /* Light gray for the heading */
    }

    #create-restaurant > input {
        margin-bottom: 1.5rem;
        padding: 0.5rem;
        border-radius: 8px;
    }

    /* Friend Section Styling (Accepted) */
    .friend-accepted {
        background-color: #D9D9D9; /* Light gray for accepted friends section */
        grid-column: 2;
        grid-row: 1/span 2;
        padding-bottom: 2em;
        border-radius: 8px;
    }

    /* Friend Section Styling (Pending) */
    .friend-pending {
        background-color: #D9D9D9; /* Light gray for pending friends section */
        grid-column: 2;
        grid-row: 3/span 2;
        border-radius: 8px;
    }

    /* General Div Styling for Sections */
    .body > div {
        background-color: #659A78; /* Olive green for sections */
        margin: 2em;
        padding: 2em;
        border-radius: 8px;
    }

    /* Link Styling */
    a {
        background-color: #659A78; /* Olive green for links */
        margin: 0.5em;
        text-decoration: none;
        color: black;
        padding: 0.2em;
        border-radius: 5px;
        transition: background-color 0.3s ease;
    }

    a:hover, button:hover {
        color: white;
        background-color: #1D5673; /* Dark blue on hover for links and buttons */
    }

    /* Restaurant Section Header */
    .restaurants {
        background-color: #B4DABA; /* Light blue for the restaurants section */
    }

    /* General Text Styling for h2, .friends, div > p */
    h2, .friends, div > p {
        background-color: #D9D9D9; /* Light gray for headings and paragraphs */
        margin: 0.2em;
        padding: 0.5rem;
        border-radius: 8px;
    }

    h6 {
        text-align: center;
        font-size: 1rem;
    }

    /* List Item Styling */
    li {
        display: flex;
    }

    /* Button Styling */
    button {
        background-color: #B4DABA; /* Light blue for buttons */
        font-size: 1rem;
        margin-bottom: 0.5rem;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 1rem;
        cursor: pointer;
    }

    /* Review Blog Styling */
    .review-blog {
        font-family: Arial, Helvetica, sans-serif;
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
    }

    .review-item {
        background-color: #f9f9f9;
        padding: 15px;
        margin-bottom: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    .review-header {
        border-bottom: 1px solid #ddd;
        padding-bottom: 10px;
        margin-bottom: 15px;
    }

    .review-header h3 {
        margin: 0;
        font-size: 24px;
        font-weight: bold;
        color: #1D5673; /* Dark blue for review title */
    }

    .review-header p {
        margin: 5px 0;
        font-size: 14px;
        color: #777;
    }

    .review-content {
        font-size: 16px;
        line-height: 1.6;
        color: #333;
    }

    .review-actions {
        text-align: right;
        margin-top: 10px;
    }

    .review-actions button {
        background-color: #ff4e4e;
        border: none;
        color: white;
        padding: 8px 15px;
        font-size: 14px;
        cursor: pointer;
        border-radius: 4px;
    }

    .review-actions button:hover {
        background-color: #ff1c1c;
    }
</style>

