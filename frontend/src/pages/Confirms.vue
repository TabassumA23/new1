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
  import { User, Restaurant, Reservation} from "../types/index";
  import { useUserStore } from "../stores/user";
  import { useUsersStore } from "../stores/users";
  import { useRestaurantsStore } from "../stores/restaurants";
  import { useReservationsStore } from "../stores/reservations";
  import {useCookies} from 'vue3-cookies';
  export default defineComponent({
    data() {
        return {
        // chosenRestaurant: "",
        // chosenReservation: "",
        // reservation: null,
        reservation: [],
        currentPage: 1,
        perPage: 5
        };
    },
    async mounted() {
      const { cookies } = useCookies();
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

        // Fetching all reservations from the backend
        let responses = await fetch(`http://localhost:8000/reservations/`);
        let reservationData = await responses.json();

        // Update the state with the fetched restaurant data
        let madeReservations = reservationData.reservations as Reservation[];
        const reservationsStore = useReservationsStore();
        reservationsStore.saveReservations(madeReservations); 
        console.log(responses)
    },
    methods: {
      getRestaurantOwnerId(restaurantId) {
          const restaurant = this.restaurants.find(r => r.id === restaurantId);
          return restaurant && restaurant.user ? restaurant.user.id : null;
      },
      async deleteReservation(reservationId: number) {
          // Check if the logged-in user is the one who wrote the review
          const reservationToDelete = this.reservations.find(reservation => reservation.id === reservationId);
          if (!reservationToDelete || reservationToDelete.user.id !== this.user.id) {
              alert("You cannot delete this restaurant. Only the author can delete it.");
              return; 
          }

          try {
              const { cookies } = useCookies();
              const response = await fetch(`http://localhost:8000/reservation/${reservationId}/`, {
                  method: 'DELETE',
                  headers: {
                      'Authorization': `Bearer ${cookies.get('access_token')}`,
                      'Content-Type': 'application/json',
                      'X-CSRFToken': cookies.get('csrftoken'),
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
              const { cookies } = useCookies();
              const response = await fetch(`http://localhost:8000/reservation/${reservation.id}/`, {
                  method: 'PUT',
                  headers: {
                      'Authorization': `Bearer ${useCookies.get('access_token')}`,
                      'Content-Type': 'application/json',
                      'X-CSRFToken': cookies.get('csrftoken'),
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
    }, 
    computed: {
      user(): User | undefined {
        const userStore = useUserStore();
        return userStore.user;
      },
      restaurants(): Restaurant[]{
        const restaurantsStore = useRestaurantsStore;
        return this.restaurantsStore.restaurants; // Bind to the fetched cuisine data from Pinia store
      },
      reservations(): Reservation[]{
        const reservationsStore = useReservationsStore;
        return this.reservationsStore.reservations; // Bind to the fetched cuisine data from Pinia store
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
        const usersStore = useUsersStore();       
        return { userStore, restaurantsStore,reservationsStore, usersStore};
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