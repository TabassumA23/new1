<template>
  <main class="reservations-page">
    <div class="card reservation-card">
      <h2>Reservations</h2>

      <div
        class="reservation-item"
        v-for="(reservation, index) in reservations"
        :key="reservation.id || index"
      >
        <div class="reservation-header">
          <h3>Restaurant: {{ reservation.restaurant.name }}</h3>
          <p>
            <strong>By:</strong> {{ reservation.user.first_name }}
          </p>
        </div>

        <div class="reservation-content">
          <p><strong>Time:</strong> {{ reservation.reservation_time }}</p>
        </div>

        <div class="reservation-content">
          <p><strong>Guests:</strong> {{ reservation.number_of_people }}</p>
        </div>

        <div class="reservation-content" v-if="getRestaurantOwnerId(reservation.restaurant.id) === user.id">
          <p><strong>Status:</strong> {{ reservation.status }}</p>
          <select v-model="reservation.status" @change="updateStatus(reservation)">
            <option value="0">Pending</option>
            <option value="1">Confirmed</option>
            <option :value="2">Declined</option>
          </select>
        </div>

        <div class="reservation-content">
          <p><strong>Special requests:</strong> {{ reservation.special_requests }}</p>
        </div>

        <div class="reservation-actions" v-if="reservation.user.id === user.id">
          <button @click="deleteReservation(reservation.id)">Delete Reservation</button>
        </div>
        
      </div>

       <!-- Pagination Controls -->
        <div class="pagination-controls">
            <button @click="currentPage--" :disabled="currentPage === 1">Previous</button>
            <span>Page {{ currentPage }} of {{ totalPages }}</span>
            <button @click="currentPage++" :disabled="currentPage === totalPages">Next</button>
        </div>
    </div>
  </main>
</template>



<script lang="ts">
  import { defineComponent } from "vue";
  import { User, Restaurant, Reservation, Friendship, Chosen,Cuisine, ChosenCuisine} from "../types/index";
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
          
          editFirstName: false,
          editLastName: false,
          editEmail: false,
          editDateOfBirth: false,
          
          editedUser: {
              first_name: "",
              last_name: "",
              email: "",
              date_of_birth: "",
              
          },

          newRestaurant: {
            name: "",
            description: "",
            rating: 0,
            seats_available: 0,
            location: "London",
          },
          chosenRestaurant: "",
          chosenReservation: "",
          reservation: null,
          chosenChosenCuisine: "",
          currentPage: 1,
          perPage: 5
          
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
        

          // Update the state with the fetched restaurant data
          let madeRestaurants = restaurantData.restaurants as Restaurant[];
          const restaurantsStore = useRestaurantsStore();
          restaurantsStore.saveRestaurants(madeRestaurants); 
          console.log(response)

          // Fetching all restaurants from the backend
          let resps = await fetch(`http://localhost:8000/reservations/`);
          let reservationData = await resps.json();
        

          // Update the state with the fetched restaurant data
          let madeReservations = reservationData.reservations as Reservation[];
          const reservationsStore = useReservationsStore();
          reservationsStore.saveReservations(madeReservations); 
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
            getRestaurantOwnerId(restaurantId) {
                const restaurant = this.restaurants.find(r => r.id === restaurantId);
                return restaurant && restaurant.user ? restaurant.user.id : null;
            },
            toggleEditField(field: string) {
            console.log(typeof field)
              this[`edit${field}`] = !this[`edit${field}`];
              if (this[`edit${field}`]) {
                  this.editedUser[field.toLowerCase()] = this.user[field.toLowerCase()];
              }
              //this.editPassword = !this.editPassword; // Toggle edit mode
          },

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
                console.error('Error deleting restaurant:', error);
                window.location.reload(); 
                if (response.ok) {
                    // Remove the deleted review from the list
                    this.restaurants = this.restaurants.filter(restaurant => restaurant.id !== restaurantId);
                    alert('Restaurant deleted successfully!');
                } else {
                    console.log("Deleting reservation with ID:", reservationId);

                    alert('Failed to delete the restaurant.');
                }
            } catch (error) {
                
                alert('Failed to delete the revirestaurantew.');
            }
        },

        async deleteReservation(reservationId: number) {
            // Check if the logged-in user is the one who wrote the review
            const reservationToDelete = this.reservations.find(reservation => reservation.id === reservationId);
            if (!reservationToDelete || reservationToDelete.user.id !== this.user.id) {
                alert("You cannot delete this restaurant. Only the author can delete it.");
                return; 
            }

            try {
                
                const response = await fetch(`http://localhost:8000/reservation/${reservationId}/`, {
                    method: 'DELETE',
                    headers: {
                        'Authorization': `Bearer ${VueCookies.get('access_token')}`,
                        'Content-Type': 'application/json',
                        'X-CSRFToken': VueCookies.get('csrftoken'),
                    },
                    credentials: 'include',
                });
                console.error('Error deleting reservation:', reservationId);
                window.location.reload(); 
                if (response.ok) {
                    // Remove the deleted review from the list
                    this.reservations = this.reservations.filter(reservation => reservation.id !== reservationId);
                    alert('Reservation deleted successfully!');
                } else {
                    alert('Failed to delete the reservation.');
                }
            } catch (error) {
                console.error('Error deleting reservation:', error);
                alert('Failed to delete reservation.');
            }
        },

        async updateStatus(reservation) {
            try {
                const payload = {
                    status: reservation.status, 
                };

                const response = await fetch(`http://localhost:8000/reservation/${reservation.id}/`, {
                    method: 'PUT',
                    headers: {
                        'Authorization': `Bearer ${VueCookies.get('access_token')}`,
                        'Content-Type': 'application/json',
                        'X-CSRFToken': VueCookies.get('csrftoken'),
                    },
                    credentials: 'include',
                    body: JSON.stringify(payload),
                });
                window.location.reload();
                const responseText = await response.text();
                console.log(responseText);

                if (response.ok) {
                    alert('Reservation status updated successfully!');
                } else {
                    alert('Failed to update reservation status');
                }
            } catch (error) {
                console.error('Error updating reservation status:', error);
                alert('Failed to update reservation status');
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
           // Accepts the pending friendship between user and friend it then makes an accepted friendship between friend and user
           //This means the friendship is symmetrical 
           async acceptFriendship(friendshipId: number) {
              try {
                  const acceptResponse = await fetch(`http://localhost:8000/friendship/${friendshipId}/`, {
                      method: "PUT",
                      headers: {
                          "Authorization": `Bearer ${VueCookies.get("access_token")}`,
                          "Content-Type": "application/json",
                          "X-CSRFToken": VueCookies.get("csrftoken"),
                      },
                      credentials: "include",
                  });

                  if (!acceptResponse.ok) {
                      throw new Error("Failed to accept friendship.");
                  }

                  const dataAccept = await acceptResponse.json();
                  const newAccept = dataAccept.friendship as Friendship;

                  // Update the friendship in the store
                  const friendshipsStore = useFriendshipsStore();
                  friendshipsStore.addFriendship(newAccept);
                  window.location.reload();
                  alert(`Accepted successfully!`);
              } catch (error) {
                  console.error("Error accepting friendship:", error);
                  alert("Failed to accept friendship. Please try again.");
              }
          },
          //rejects the friendships between users and friend whether pending or accepted
          async deleteFriendship(friendshipId: number) {
            console.log(friendshipId)
            try {
              const response = await fetch(`http://localhost:8000/friendship/${friendshipId}/`, {
                method: "DELETE",
                headers: {
                  "Authorization": `Bearer ${VueCookies.get("access_token")}`,
                  "Content-Type": "application/json",
                  "X-CSRFToken": VueCookies.get("csrftoken"),
                },
                credentials: "include",
              });

              if (!response.ok) {
                throw new Error("Failed to delete friendship");
              }

              //Remove the deleted friendship from the store
              const friendshipsStore = useFriendshipsStore();
              friendshipsStore.removeFriendship(friendshipId);

              window.location.reload();
              alert("Friendship deleted successfully!");
            } catch (error) {
              console.error("Error deleting friendship:", error);
              alert("Failed to delete friendship. Please try again.");
            }
          },
          //deletes the friendships between users and friend whether pending or accepted
          async deleteChosenCuisine(chosenCuisineId: number) {
       
            try {
              const response = await fetch(`http://localhost:8000/chosenCuisine/${chosenCuisineId}/`, {
                method: "DELETE",
                headers: {
                  "Authorization": `Bearer ${VueCookies.get("access_token")}`,
                  "Content-Type": "application/json",
                  "X-CSRFToken": VueCookies.get("csrftoken"),
                },
                credentials: "include",
              });

              if (!response.ok) {
                throw new Error("Failed to delete chosen cuisine");
              }

              //Remove the deleted friendship from the store
              const chosenCuisinesStore = useChosenCuisinesStore();
              //chosenCuisinesStore.removeChosenCuisine(chosenCuisineId);

              window.location.reload();
              alert("Chosen cuisine deleted successfully!");
            } catch (error) {
              console.error("Error deleting chosen cuisine:", error);
              alert("Failed to delete chosen cuisine. Please try again.");
            }
          },

          async addChosenCuisine() {
            if (this.chosenChosenCuisine === "") {
                alert("Invalid cuisine Choice.");
                return;
            }

            const chosenCuisinesStore = useChosenCuisinesStore();
            const cuisinesStore = useCuisinesStore();
            const chosenChosenCuisineLower = this.chosenChosenCuisine.toLowerCase();

            // Check if the logged-in user has already chosen this cusine
            let alreadyChosenCuisineByUser = chosenCuisinesStore.chosenCuisines.some(chosenCuisine => chosenCuisine.user === this.user.id && chosenCuisine.name.toLowerCase() === chosenChosenCuisineLower);
            
            if (alreadyChosenCuisineByUser) {
                alert("You have already chosen this cuisine.");
                return;
            }

            // Find the cuisine from the cuisine store
            let foundCuisine = cuisinesStore.getCuisineByName(this.chosenChosenCuisine);
            if (!foundCuisine) {
                alert("cuisine not found.");
                return;
            }

            const foundCuisineId = foundCuisine.id;

            // Prepare the payload for creating a new chosen cuisine
            const payload = {
                user_id: this.user.id,
                cuisine_id: foundCuisineId,
            };

            // Send POST request to create a chosen cuisine
            const chosenCuisineResponse = await fetch("http://localhost:8000/chosenCuisines/", {
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
            if (chosenCuisineResponse.ok) {
                const dataC = await chosenCuisineResponse.json();
                const createdChosenCuisine = dataC.chosenCuisine as ChosenCuisine;
                //chosenCuisinesStore.addChosenCuisine(createdChosenCuisine);

                window.location.reload(); // Refresh the page to reflect the changes
                alert("Chosen cuisine added successfully!");
            } else {
                alert("Failed to add the chosen cuisine. Please try again.");
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
          cuisines(): Cuisine[]{
              const cuisinesStore = useCuisinesStore;
              return this.cuisinesStore.cuisines; // Bind to the fetched cuisine data from Pinia store
          },
          friendships(){
              const friendshipsStore = useFriendshipsStore;
              return this.friendshipsStore.friendships;
          },
          chosens(){
              const chosensStore = useChosensStore;
              return this.chosensStore.chosens;
          },
          chosenCuisines(){
              const chosenCuisinesStore = useChosenCuisinesStore;
              return this.chosenCuisinesStore.chosenCuisines;
          },
          totalPages() {
            return Math.ceil(this.reservations.length / this.perPage);
            },
            paginatedReservations() {
            const start = (this.currentPage - 1) * this.perPage;
            return this.reservations.slice(start, start + this.perPage);
            }
    
      },
      setup() {
          const userStore = useUserStore();
          const restaurantsStore = useRestaurantsStore();
          const reservationsStore = useReservationsStore();
          const cuisinesStore = useCuisinesStore();
          const friendshipsStore = useFriendshipsStore();
          const usersStore = useUsersStore();
          const chosensStore = useChosensStore();
          const chosenCuisinesStore = useChosenCuisinesStore();
          return { userStore , restaurantsStore, reservationsStore , friendshipsStore, usersStore, chosensStore, chosenCuisinesStore, cuisinesStore};
      },
  });
  </script>


<style scoped>
  :root {
    --bg-start: #0f0c29;
    --bg-end: #302b63;
    --card-bg: rgba(255, 255, 255, 0.05);
    --accent: #ff00c1;
    --text: #eee;
    --muted: #aaa;
    --radius: 12px;
  }

  .reservations-page {
    background: linear-gradient(135deg, var(--bg-start), var(--bg-end));
    min-height: 100vh;
    padding: 2rem;
    font-family: 'Segoe UI', sans-serif;
    color: var(--text);
  }

  .card.reservation-card {
    background: var(--card-bg);
    padding: 1.5rem;
    border-radius: var(--radius);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
  }

  .reservations-page h2 {
    margin-bottom: 1rem;
    color: var(--text);
  }

  .reservation-item {
    background: var(--card-bg);
    margin: 1rem 0;
    padding: 1rem;
    border-radius: var(--radius);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
  }

  .reservation-header h3 {
    margin: 0 0 0.5rem;
    color: var(--accent);
    font-size: 1.4rem;
  }

  .reservation-header p {
    margin: 0;
    color: var(--muted);
    font-size: 0.9rem;
  }

  .reservation-content p {
    margin: 0.5rem 0;
    color: var(--text);
    font-size: 1rem;
  }

  select {
    background: rgba(255, 255, 255, 0.1);
    border: 2px solid #ff8c00;
    border-radius: 10px;
    padding: 0.5rem;
    color: #000;
    font-size: 1rem;
    outline: none;
    margin-top: 0.25rem;
    transition: border-color 0.2s, box-shadow 0.2s;
  }

  select:focus {
    border-color: var(--accent);
    box-shadow: 0 0 0 3px rgba(255, 0, 193, 0.2);
  }

  .reservation-actions {
    text-align: right;
    margin-top: 1rem;
  }

  .reservation-actions button {
    background: linear-gradient(90deg, #ff0080, #ff8c00);
    border: none;
    padding: 0.5rem 1rem;
    color: #fff;
    font-weight: 600;
    border-radius: var(--radius);
    cursor: pointer;
    transition: transform 0.15s ease, opacity 0.2s;
  }

  .reservation-actions button:hover {
    transform: scale(1.05);
    opacity: 0.9;
  }

  .pagination-controls {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 1rem;
    margin-top: 1rem;
  }

  .pagination-controls button {
    background: linear-gradient(90deg, #ff0080, #ff8c00);
    color: #fff;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 8px;
    cursor: pointer;
  }

  .pagination-controls button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  @media (min-width: 600px) {
    .reservation-item {
      margin: 1rem 0;
    }
  }
</style>