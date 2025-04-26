<template>
  <div class="body">
    <div class="reservation-form">
        <h3>Create a Reservation</h3>
        <label for="restaurant">Select Restaurant:</label>
        <select id="restaurants" v-model="newReservation.restaurant">
        <option v-for="restaurant in restaurants" :key="restaurant.id" :value="restaurant">
            {{ restaurant.name }}
        </option>
        </select>

        <label for="reservation-time">Choose reservation time:</label>
        <input type="datetime-local" v-model="newReservation.reservation_time" />


        <label for="number-of-people">Number of People:</label>
        <input type="number" v-model="newReservation.number_of_people" />

        
        <label for="special-requests">Addition notes:</label>
        <input type="special-requests" v-model="newReservation.special_requests" />

        <button @click="createReservation">Special requests:</button>
  </div>
  </div>
</template>

<script lang="ts">
  import { defineComponent } from "vue";
  import { User, Restaurant, Chosen, Reservation} from "../types/index";
  import { useUserStore } from "../stores/user";
  import { useUsersStore } from "../stores/users";
  import { useRestaurantsStore } from "../stores/restaurants";
  import { useReservationsStore } from "../stores/reservations";
  import { useChosenStore } from "../stores/chosen";
  import { useChosensStore } from "../stores/chosens";

  import VueCookies from 'vue-cookies';

  


  export default defineComponent({
      data() {
          return {
          
          newReservation: {
          restaurant: null,          
          reservation_time: "",      
          number_of_people: 0,      
          special_requests: "",     
          status: 0,               
          },
          chosenRestaurant: "",
          
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

          //fetch all the friendships
          let responseChosen = await fetch("http://localhost:8000/chosens/");
          let dataChosen = await responseChosen.json();
          let chosens = dataChosen.chosens as Chosen[];
  
          const storeChosens = useChosensStore();
          storeChosens.saveChosens(chosens);

           // Fetching all reservations from the backend
            const res = await fetch('http://localhost:8000/reservations/');
            const data = await res.json();
            this.reservations = data.reservations;  // Make sure the backend sends an array of reservations

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
        async createReservation() {
            const reservationsStore = useReservationsStore();
            const userId = this.userStore.user.id;

            // Validate if the restaurant is selected correctly
            if (!this.newReservation.restaurant || !this.newReservation.restaurant.id) {
                alert("Please select a valid restaurant.");
                return;
            }

            // Validate if the reservation time is set correctly
            if (!this.newReservation.reservation_time) {
                alert("Please select a valid reservation time.");
                return;
            }

            const payload = {
                restaurant_id: this.newReservation.restaurant.id, 
                reservation_time: this.newReservation.reservation_time,
                number_of_people: this.newReservation.number_of_people,
                status: 0,
                special_requests: this.newReservation.special_requests || "",
                user_id: userId,
            };

            console.log(payload); 
            console.log(userId);

            try {
                const reservationResponse = await fetch('http://localhost:8000/reservations/', {
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
                    const data = await reservationResponse.json();
                    const createdReservation = data.reservation;  // Ensure that the response has reservation data
                    reservationsStore.addReservation(createdReservation);  // Add to the Pinia store
                    window.location.reload();
                    alert('Reservation added successfully!');
               //} else {
                    //alert('Failed to create reservation');
                //}
            } catch (error) {
                console.error('Error creating reservation:', error);
                alert('Failed to create reservation');
            }
        },


        async deleteReservation(reservationId: number) {
            // Check if the logged-in user is the one who wrote the reservation
            const reservationToDelete = this.reservations.find(reservation => reservation.id === reservationId);
            if (!reservationToDelete || reservationToDelete.user.id !== this.user.id) {
                alert("You cannot delete this reservation. Only the author can delete it.");
                return; // Prevent deletion
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

                if (response.ok) {
                    // Remove the deleted reservation from the list
                    this.reservations = this.reservations.filter(reservation => reservation.id !== reservationId);
                    alert('Reservation deleted successfully!');
                } else {
                    alert('Failed to delete the reservation.');
                }
            } catch (error) {
                console.error('Error deleting reservation:', error);
                alert('Failed to delete the reservation.');
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
          reservations(): Reservation[]{
              const reservationsStore = useReservationsStore;
              return this.reservationsStore.reservations; // Bind to the fetched cuisine data from Pinia store
          },
          
          chosens(){
              const chosensStore = useChosensStore;
              return this.chosensStore.chosens;
          },
    
      },
      setup() {
          const userStore = useUserStore();
          const restaurantsStore = useRestaurantsStore();
          const reservationsStore = useReservationsStore();
          
         
          const usersStore = useUsersStore();
          const chosensStore = useChosensStore();
          
          return { userStore , restaurantsStore , usersStore, chosensStore, reservationsStore};
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

  .body {
    background: linear-gradient(135deg, var(--bg-start), var(--bg-end));
    min-height: 100vh;
    font-family: 'Segoe UI', sans-serif;
    color: var(--text);
    padding: 2rem;
    display: flex;
    justify-content: center;
  }

  .reservation-form {
    background: var(--card-bg);
    padding: 2rem;
    border-radius: var(--radius);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    max-width: 500px;
    width: 100%;
    display: flex;
    flex-direction: column;
  }

  h2, h3, label {
    color: var(--text);
    margin-bottom: 0.5rem;
  }

  label {
    font-size: 1rem;
    color: var(--muted);
    margin-top: 1rem;
  }

  input,
  select {
    border: 2px solid #ff8c00;
    outline: none;
    background: rgba(255, 255, 255, 0.07);
    color: #000;
    font-size: 1rem;
    padding: 0.75rem;
    border-radius: 10px;
    margin-bottom: 1rem;
    width: 100%;
  }

  input:focus,
  select:focus {
    border-color: var(--accent);
    background: rgba(255, 255, 255, 0.1);
    box-shadow: 0 0 0 3px rgba(255, 0, 193, 0.2);
  }

  button {
    background: linear-gradient(90deg, #ff0080, #ff8c00);
    border: none;
    padding: 0.75rem 1.5rem;
    color: #fff;
    font-weight: 600;
    border-radius: var(--radius);
    cursor: pointer;
    transition: transform 0.15s ease;
    margin-top: 1rem;
  }

  button:hover {
    transform: scale(1.05);
  }
</style>


