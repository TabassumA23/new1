<template>
  <div class="body">
    <div class="reservation-form">
      <h2>Welcome {{ user.first_name }}</h2>
        <h2>Create a Restaurant</h2>

        <label for="restaurant-name">Restaurant name:</label>
        <input type="name" v-model="newRestaurant.name" />

        <label for="cuisine">Select Cuisine:</label>
        <select id="cuisines" v-model="newRestaurant.cuisine">
        <option v-for="cuisine in cuisines" :key="cuisine.id" :value="cuisine">
            {{ cuisine.name }}
        </option>
        </select>

        <label for="allergys">Allergies:</label>
        <select v-model="newRestaurant.allergy" class="form-control" id="allergys" multiple>
          <option v-for="(allergy, index) in allergys" :key="index" :value="allergy.id">
            {{ allergy.name }}
          </option>
        </select>


        <label for="rating">Rating:</label>
        <input type="rating" v-model="newRestaurant.rating" />


        <label for="seats-available">Seats Available:</label>
        <input type="number" v-model="newRestaurant.seats_available" />

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

        <!-- <label for="special-requests">Addition notes:</label>
        <input type="special-requests" v-model="newReservation.special_requests" /> -->

        <button @click="createRestaurant">Create Restaurant</button>
  </div>

   <div
        class="restaurant-item"
        
        v-for="(restaurant, index) in restaurants"
        :key="index"
        
    >
        <div class="restaurant-header">
          <h3>restaurant: {{ restaurant.name }}</h3>
          <p>
            <!-- <strong>By:</strong> {{ reservation.user.id }}  -->
            <!-- | <strong>Date:</strong> {{ formatDate(restaurant.date) }} -->
          </p>
        </div>

        <div class="restaurant-content">
          <p>cuisine: {{ restaurant.cuisine }}</p>
        </div>

        <div class="restaurant-content">
        <p>Allergies:
          <span v-for="(allergy, index) in restaurant.allergys" :key="index">
            {{ allergy }}{{ index < restaurant.allergys.length - 1 ? ', ' : '' }}
          </span>
        </p>
      </div>
        <!-- <div class="restaurant-content" v-for="(restaurant, index) in restaurants" :key="index">
            
            <div v-if="restaurant.user.id === user.id">
                <p>Status: {{ reservation.status }}
                <select v-model="reservation.status" @change="updateStatus(reservation)">
                    <option value="0">Pending</option>
                    <option value="1">Confirmed</option>
                </select>
                </p>
            </div>
            
        </div> -->

        <div class="restaurant-content">
          <p>rating: {{ restaurant.rating }}</p>
        </div>

        <div class="restaurant-content">
          <p>location: {{ restaurant.location }}</p>
        </div>

        <div class="restaurant-content">
          <p>seats available: {{ restaurant.seats_available }}</p>
        </div>

        <div class="restaurant-actions" v-if="restaurant.user.id === user.id">
          <button @click="deleteRestaurant(restaurant.id)">Delete restaurant</button>
        </div>
      </div>
    </div>
  
</template>

<script lang="ts">
  import { defineComponent } from "vue";
  import { User, Restaurant, Chosen, Cuisine, Allergy} from "../types/index";
  import { useUserStore } from "../stores/user";
  import { useUsersStore } from "../stores/users";
  import { useRestaurantsStore } from "../stores/restaurants";
  import { useCuisinesStore } from "../stores/cuisines";
  import { useAllergysStore } from "../stores/allergys";
  import { useChosenStore } from "../stores/chosen";
  import { useChosensStore } from "../stores/chosens";

  import VueCookies from 'vue-cookies';

  


  export default defineComponent({
      data() {
          return {
          
          newRestaurant: {
          name: "",          // Will hold the selected restaurant object
          cuisine: null,     // Will hold the reservation time
          allergy: [],      // Will hold the number of people
          rating: 0,     // Will hold any special requests (optional)
          seats_available: 0,
          location: "London"                // Will hold the reservation status (default to 'pending', 0)
          },
          chosenRestaurant: "",
          restaurant: null,
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
         
          // Fetching all cuisines from the backend
          let response = await fetch(`http://localhost:8000/cuisines/`);
          let cuisineData = await response.json();
        

          // Update the state with the fetched restaurant data
          let madeCuisines = cuisineData.cuisines as Cuisine[];
          const cuisinesStore = useCuisinesStore();
          cuisinesStore.saveCuisines(madeCuisines); 
          console.log(response)

          // Fetching all allergys from the backend
          let responseC = await fetch(`http://localhost:8000/allergys/`);
          let allergyData = await responseC.json();
        

          // Update the state with the fetched restaurant data
          let madeAllergys = allergyData.allergys as Allergy[];
          const allergysStore = useAllergysStore();
          allergysStore.saveAllergys(madeAllergys); 
          console.log(responseC)

          //fetch all the friendships
          let responseChosen = await fetch("http://localhost:8000/chosens/");
          let dataChosen = await responseChosen.json();
          let chosens = dataChosen.chosens as Chosen[];
  
          const storeChosens = useChosensStore();
          storeChosens.saveChosens(chosens);

          //  // Fetching all restaurants from the backend
          //   const res = await fetch('http://localhost:8000/restaurants/');
          //   const data = await res.json();
          //   this.restaurants = data.restaurants;  // Make sure the backend sends an array of restaurants

          // Fetching all restaurants from the backend
          let responseR = await fetch(`http://localhost:8000/restaurants/`);
          let restaurantData = await responseR.json();
        

          // Update the state with the fetched restaurant data
          let madeRestaurants = restaurantData.restaurants as Restaurant[];
          const restaurantsStore = useRestaurantsStore();
          restaurantsStore.saveRestaurants(madeRestaurants); 
          console.log(responseR)

      },
      methods: {
          
          
          async saveField(field: string) {
             
              try {
                  
                  const payload = {
                      [field.toLowerCase()]: this.editedUser[field.toLowerCase()],
                  };
                  console.log(payload)
                  const response = await fetch(`http://localhost:8000/user/${this.user.id}/`, {
                      method: "PUT",
                      headers: {
                          'Authorization': `Bearer ${VueCookies.get('access_token')}`,
                          'Content-Type': 'application/json',
                          'X-CSRFToken': VueCookies.get('csrftoken'),
                      },
                      credentials: 'include',
                      body: JSON.stringify(payload),
                  });
              
                  console.log("CSRF Token:", this.userStore.csrf);

                  if (!response.ok) {
                      throw new Error("Failed to update field");
                  }

                  const updatedUser = await response.json();
                  console.log(updatedUser)
                  this.userStore = this.userStore.saveUsers(updatedUser); // Update the user state in the store
                  window.location.reload();
                  alert(`${field} updated successfully!`);
              } catch (error) {
                  console.error(error);
                  alert(`Failed to update ${field}.`);
              }
          },
        


         /* Creating a New review */
        async createRestaurant() {
            const restaurantsStore = useRestaurantsStore();
            const userId = this.userStore.user.id;

            // Validate if the restaurant is selected correctly
            // if (!this.newRestaurant.cusine || !this.newRestaurant.cuisine.id) {
            //     alert("Please select a valid cusine.");
            //     return;
            // }

            // Validate if the reservation time is set correctly
            // if (!this.newReservation.reservation_time) {
            //     alert("Please select a valid reservation time.");
            //     return;
            // }

            const payload = {
                cuisine_id: this.newRestaurant.cuisine.id, 
                allergy_ids: this.newRestaurant.allergy, 
                name: this.newRestaurant.name,
                seats_available: this.newRestaurant.seats_available,
                rating: this.newRestaurant.rating,
                location: this.newRestaurant.location,
                user_id: userId,
            };

            console.log(payload); 
            console.log(userId);

            try {
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

                //const responseText = await reservationResponse.text();  // Log raw response for debugging
               // console.log(responseText);

                //if (reservationResponse.ok) {
                    const data = await restaurantResponse.json();
                    const createdRestaurant = data.restaurant;  // Ensure that the response has reservation data
                    restaurantsStore.addRestaurant(createdRestaurant);  // Add to the Pinia store
                    window.location.reload();
                    alert('Restaurant added successfully!');
               //} else {
                    //alert('Failed to create reservation');
                //}
            } catch (error) {
                console.error('Error creating restaurant:', error);
                alert('Failed to create restaurant');
            }
        },


        async deleteRestaurant(restaurantId: number) {
            // Check if the logged-in user is the one who wrote the reservation
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

                if (response.ok) {
                    // Remove the deleted reservation from the list
                    this.restaurants = this.restaurants.filter(restaurant => restaurant.id !== restaurantId);
                    alert('Restaurant deleted successfully!');
                    window.location.reload();
                } else {
                    alert('Failed to delete the restaurant.');
                }
            } catch (error) {
                console.error('Error deleting restaurant:', error);
                alert('Failed to delete the restaurant.');
            }
        },
          //deletes the friendships between users and friend whether pending or accepted
          async deleteChosen(chosenId: number) {
       
            try {
              const response = await fetch(`http://localhost:8000/chosen/${chosenId}/`, {
                method: "DELETE",
                headers: {
                  "Authorization": `Bearer ${VueCookies.get("access_token")}`,
                  "Content-Type": "application/json",
                  "X-CSRFToken": VueCookies.get("csrftoken"),
                },
                credentials: "include",
              });

              if (!response.ok) {
                throw new Error("Failed to delete chosen restaurant");
              }

              //Remove the deleted friendship from the store
              const chosensStore = useChosensStore();
              chosensStore.removeChosen(chosenId);

              window.location.reload();
              alert("Chosen restaurant deleted successfully!");
            } catch (error) {
              console.error("Error deleting chosen restaurant:", error);
              alert("Failed to delete chosen restaurant. Please try again.");
            }
          },

          async addChosen() {
            if (this.chosenRestaurant === "") {
                alert("Invalid restaurant Choice.");
                return;
            }

            const chosensStore = useChosensStore();
            const restaurantsStore = useRestaurantsStore();
            const chosenRestaurantLower = this.chosenRestaurant.toLowerCase();

            // Check if the logged-in user has already chosen this restaurant
            let alreadyChosenByUser = chosensStore.chosens.some(chosen => chosen.user === this.user.id && chosen.name.toLowerCase() === chosenRestaurantLower);
            
            if (alreadyChosenByUser) {
                alert("You have already chosen this restaurant.");
                return;
            }

            // Find the restaurant from the restaurant store
            let foundRestaurant = restaurantsStore.getRestaurantByName(this.chosenRestaurant);
            if (!foundRestaurant) {
                alert("restaurant not found.");
                return;
            }

            const foundRestaurantId = foundRestaurant.id;

            // Prepare the payload for creating a new chosen restaurant
            const payload = {
                user_id: this.user.id,
                restaurant_id: foundRestaurantId,
            };

            // Send POST request to create a chosen restaurant
            const chosenResponse = await fetch("http://localhost:8000/chosens/", {
                method: "POST",
                headers: {
                Authorization: `Bearer ${VueCookies.get("access_token")}`,
                "Content-Type": "application/json",
                "X-CSRFToken": VueCookies.get("csrftoken"),
                },
                credentials: "include",
                body: JSON.stringify(payload),
            });

            // If the response is successful, add the new chosen restaurant to the store
            if (chosenResponse.ok) {
                const data = await chosenResponse.json();
                const createdChosen = data.chosen as Chosen;
                chosensStore.addChosen(createdChosen);

                window.location.reload(); // Refresh the page to reflect the changes
                alert("Chosen restaurant added successfully!");
            } else {
                alert("Failed to add the chosen restaurant. Please try again.");
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
          cuisines(): Cuisine[]{
              const cuisinesStore = useCuisinesStore;
              return this.cuisinesStore.cuisines; // Bind to the fetched cuisine data from Pinia store
          },
          allergys(): Allergy[]{
              const allergysStore = useAllergysStore;
              return this.allergysStore.allergys; // Bind to the fetched cuisine data from Pinia store
          },
          
          chosens(){
              const chosensStore = useChosensStore;
              return this.chosensStore.chosens;
          },
    
      },
      setup() {
          const userStore = useUserStore();
          const restaurantsStore = useRestaurantsStore();
          const allergysStore = useAllergysStore();
          const cuisinesStore = useCuisinesStore();
          const usersStore = useUsersStore();
          const chosensStore = useChosensStore();
          
          return { userStore , restaurantsStore , usersStore, chosensStore, cuisinesStore, allergysStore};
      },
  });
</script>





<style scoped>
  textarea,
  input {
    border: 2px solid #ff8c00; /* Or whatever accent color matches your theme */
    outline: none;
    background: rgba(255, 255, 255, 0.07); /* subtle contrast but not white */
    color: #fff;
    font-size: 1rem;
    padding: 0.75rem;
    border-radius: 10px;
    margin-bottom: 1rem;
    width: 100%;
  }

  textarea:focus,
  input:focus {
    border-color: #ff00c1; /* highlight border on focus */
    background: rgba(255, 255, 255, 0.1);
    box-shadow: 0 0 0 3px rgba(255, 0, 193, 0.2); /* soft glow */
  }
  :root {
    --bg-start: #0f0c29;
    --bg-end:   #302b63;
    --card-bg:  rgba(255,255,255,0.05);
    --accent:   #ff00c1;
    --text:     #eee;
    --muted:    #aaa;
    --radius:   12px;
  }

  /* Page grid & background */
  .body {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
    min-height: 100vh;
    padding: 2rem;
    background: linear-gradient(135deg, var(--bg-start), var(--bg-end));
    font-family: 'Segoe UI', sans-serif;
    color: var(--text);
  }

  /* Profile box */
  #profile-box {
    background: var(--card-bg);
    padding: 1.5rem;
    border-radius: var(--radius);
    box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    grid-column: 1;
  }

  /* “Create Restaurant” form card */
  .reservation-form {
    background: var(--card-bg);
    padding: 1.5rem;
    border-radius: var(--radius);
    box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    display: flex;
    flex-direction: column;
    gap: 1rem;
    grid-column: 2;
    max-width: 480px;
    width: 100%;
    margin: 0 auto;
  }

  /* Section headings */
  #profile-box h2,
  .reservation-form h2 {
    margin: 0;
    border-bottom: 1px solid rgba(255,255,255,0.2);
    padding-bottom: 0.5rem;
    color: var(--text);
    font-size: 1.8rem;
  }

  /* Form labels */
  .reservation-form label {
    color: var(--muted);
    font-size: 1rem;
    margin-top: 1rem;
  }

  /* Inputs & selects */
  .reservation-form input,
  .reservation-form select {
    width: 100%;
    padding: 0.6rem 0.8rem;
    background: rgba(255,255,255,0.1);
    border: none;
    border-radius: var(--radius);
    color: var(--text);
    font-size: 1rem;
    box-sizing: border-box;
  }

  /* Multi‑select scroll hint */
  .reservation-form select[multiple] {
    height: 6rem;
  }

  /* Neon gradient button */
  .reservation-form button {
    background: linear-gradient(90deg, #ff0080, #ff8c00);
    border: none;
    border-radius: var(--radius);
    padding: 0.7rem 1.2rem;
    color: #fff;
    font-weight: 600;
    cursor: pointer;
    transition: transform .15s ease;
    margin-top: 1rem;
  }
  .reservation-form button:hover {
    transform: scale(1.05);
  }

  /* List of existing restaurants */
  .restaurant-item {
    background: var(--card-bg);
    padding: 1rem;
    border-radius: var(--radius);
    box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    margin: 1rem 0;
    grid-column: 1 / span 2;
  }

  /* Restaurant headers */
  .restaurant-header h3 {
    margin: 0;
    color: var(--accent);
  }

  /* Restaurant details */
  .restaurant-content p {
    color: var(--text);
    margin: 0.5rem 0;
  }

  /* Delete button */
  .restaurant-actions button {
    background: #ff4e4e;
    border: none;
    border-radius: var(--radius);
    color: #fff;
    padding: 0.5rem 1rem;
    cursor: pointer;
    transition: background .2s ease;
  }
  .restaurant-actions button:hover {
    background: #ff1c1c;
  }

  /* Responsive: single column on narrow screens */
  @media (max-width: 800px) {
    .body {
      grid-template-columns: 1fr;
    }
    .reservation-form {
      grid-column: auto;
    }
    #profile-box {
      grid-column: auto;
    }
    .restaurant-item {
      grid-column: auto;
    }
  }
</style>


