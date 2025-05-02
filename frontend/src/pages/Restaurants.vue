<template>
  <main class="restaurant-page">
    <!-- Create Restaurant Card -->
    <div class="card restaurant-card">
      <h3>Create a New Restaurant</h3>
      <label for="restaurant-name">Restaurant name:</label>
      <input id="restaurant-name" type="text" v-model="newRestaurant.name" placeholder="Type restaurant name..." />

      <label for="cuisine">Select Cuisine:</label>
      <select id="cuisine" v-model="newRestaurant.cuisine">
        <option v-for="c in cuisines" :key="c.id" :value="c">{{ c.name }}</option>
      </select>

      <label for="allergies">Allergies:</label>
      <select id="allergies" v-model="newRestaurant.allergy" multiple>
        <option v-for="a in allergys" :key="a.id" :value="a.id">{{ a.name }}</option>
      </select>

      <label for="rating">Rating:</label>
      <input id="rating" type="number" v-model="newRestaurant.rating" placeholder="0 - 5" />

      <label for="seats">Seats Available:</label>
      <input id="seats" type="number" v-model="newRestaurant.seats_available" placeholder="Number of seats" />

      <label for="location">Location:</label>
      <select id="location" v-model="newRestaurant.location">
        <option>London</option>
        <option>Manchester</option>
        <option>Leeds</option>
        <option>Liverpool</option>
        <option>Sheffield</option>
        <option>Bristol</option>
        <option>Nottingham</option>
      </select>

      <button @click="createRestaurant">Add Restaurant</button>
    </div>

    <!-- Filters -->
    <div class="card restaurant-card filter-card">
      <h3>Filter Restaurants</h3>
      <label for="filter-name">By Name:</label>
      <input id="filter-name" type="text" v-model="filterName" placeholder="Search by name..." />

      <label for="filter-cuisine">By Cuisine:</label>
      <select id="filter-cuisine" v-model="filterCuisine">
        <option value="">All Cuisines</option>
        <option v-for="c in cuisines" :key="c.id" :value="c.name">{{ c.name }}</option>
      </select>
    </div>

    <!-- All Restaurants Listing -->
    <h2 >All Restaurants</h2>
    <div class="card restaurant-card">
      <div
        class="restaurant-item"
        v-for="r in paginatedRestaurants"
        :key="r.id"
      >
        <!-- EDIT MODE -->
        <div v-if="editingId === r.id" class="edit-form">
          <input v-model="editedRestaurant.name" placeholder="Name" />

          <select v-model="editedRestaurant.cuisine_id">
            <option
              v-for="c in cuisines"
              :key="c.id"
              :value="c.id"
            >{{ c.name }}</option>
          </select>

          <select v-model="editedRestaurant.allergy_ids" multiple>
            <option
              v-for="a in allergys"
              :key="a.id"
              :value="a.id"
            >{{ a.name }}</option>
          </select>

          <input
            type="number"
            v-model="editedRestaurant.rating"
            placeholder="Rating"
          />
          <input
            type="number"
            v-model="editedRestaurant.seats_available"
            placeholder="Seats"
          />
          <select v-model="editedRestaurant.location">
            <!-- your location options -->
            <option>London</option>
            <option>Manchester</option>
            <!-- …etc… -->
          </select>

          <button @click="saveRestaurant(r.id)">Save</button>
          <button @click="cancelEdit()">Cancel</button>
        </div>

        <!-- READ-ONLY MODE -->
        <div v-else class="restaurant-content">
          <h3>{{ r.name }}</h3>
          <p><strong>Cuisine:</strong> {{ cuisineName(r) }}</p>
          <p>
            <strong>Allergies:</strong>
            {{ r.allergys.map(a => allergyName(a)).join(', ') }}
          </p>
          <p><strong>Rating:</strong> {{ r.rating }}</p>
          <p><strong>Seats:</strong> {{ r.seats_available }}</p>
          <p><strong>Location:</strong> {{ r.location }}</p>

          <div class="restaurant-actions" v-if="r.user.id === user.id">
            <button @click="startEdit(r)">Edit</button>
            <button @click="deleteRestaurant(r.id)">Delete</button>
          </div>
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
          location: "London",              // Will hold the reservation status (default to 'pending', 0)
          },
          chosenRestaurant: "",
          restaurant: null,
          currentPage: 1,
          perPage: 3,
          filterName: '',
          filterCuisine: '',
          filterAllergy: '',
          editingId: null as number|null,
          editedRestaurant: {
            name: '',
            cuisine_id: 0,
            allergy_ids: [] as number[],
            rating: 0,
            seats_available: 0,
            location: '',
          },
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
        startEdit(r: Restaurant) {
          this.editingId = r.id
          this.editedRestaurant = {
            name: r.name,
            cuisine_id: typeof r.cuisine === 'object' ? r.cuisine.id : r.cuisine,
            allergy_ids: r.allergys.map(a => a.id ?? a) as number[],
            rating: r.rating,
            seats_available: r.seats_available,
            location: r.location,
          }
        },
        cancelEdit() {
          this.editingId = null
        },
        async saveRestaurant(id: number) {
          try {
            const payload = {
              name: this.editedRestaurant.name,
              cuisine_id: this.editedRestaurant.cuisine_id,
              allergy_ids: this.editedRestaurant.allergy_ids,
              rating: this.editedRestaurant.rating,
              seats_available: this.editedRestaurant.seats_available,
              location: this.editedRestaurant.location,
            }
            const res = await fetch(`http://localhost:8000/restaurant/${id}/`, {
              method: 'PUT',
              headers: {
                'Authorization': `Bearer ${VueCookies.get('access_token')}`,
                'Content-Type': 'application/json',
                'X-CSRFToken': VueCookies.get('csrftoken'),
              },
              credentials: 'include',
              body: JSON.stringify(payload),
            })
            if (!res.ok) throw new Error('Update failed')
            const { restaurant: updated } = await res.json()
            // update Pinia store
            this.restaurantsStore.updateRestaurant(updated)
            this.editingId = null
            alert('Restaurant updated!')
          } catch (e) {
            console.error(e)
            alert('Could not save changes.')
          }
        },
        cuisineName(restaurant) {
          return restaurant.cuisine && restaurant.cuisine.name
            ? restaurant.cuisine.name
            : restaurant.cuisine;
        },
        allergyName(allergy) {
          return allergy && allergy.name ? allergy.name : allergy;
        },
          
          
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
          filteredRestaurants() {
            return this.restaurants.filter(r => {
              const matchesName = r.name.toLowerCase().includes(this.filterName.toLowerCase());
              const cName = this.cuisineName(r);
              const matchesCuisine = this.filterCuisine ? cName === this.filterCuisine : true;
              const allergyList = r.allergys.map(a => this.allergyName(a));
              const matchesAllergy = this.filterAllergy ? allergyList.includes(this.filterAllergy) : true;
              return matchesName && matchesCuisine && matchesAllergy;
            });
          },
          // Total pages based on filtered results
          totalPages() {
            return Math.ceil(this.filteredRestaurants.length / this.perPage) || 1;
          },
          // Slice filtered results for current page
          paginatedRestaurants() {
            const start = (this.currentPage - 1) * this.perPage;
            return this.filteredRestaurants.slice(start, start + this.perPage);
          }
    
      },
      watch: {
        filterName() { this.currentPage = 1; },
        filterCuisine() { this.currentPage = 1; },
        filterAllergy() { this.currentPage = 1; }
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
  :root {
    --bg-start: #0f0c29;
    --bg-end: #302b63;
    --card-bg: rgba(255, 255, 255, 0.05);
    --accent: #ff00c1;
    --text: #eee;
    --muted: #aaa;
    --radius: 12px;
  }

  .restaurant-page {
    background: linear-gradient(135deg, var(--bg-start), var(--bg-end));
    min-height: 100vh;
    padding: 2rem;
    font-family: 'Segoe UI', sans-serif;
    color: var(--text);
  }

  .card.restaurant-card {
    background: var(--card-bg);
    padding: 1.5rem;
    border-radius: var(--radius);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    margin-bottom: 2rem;
  }

  .filter-card {
    margin-top: 0;
  }

  h2, h3 {
    margin-bottom: 1rem;
    color: var(--text);
  }

  label {
    display: block;
    margin-top: 1rem;
    color: var(--muted);
    font-size: 1rem;
  }

  input, select {
    width: 100%;
    padding: 0.75rem;
    margin-top: 0.5rem;
    background: rgba(255, 255, 255, 0.07);
    border: 2px solid #ff8c00;
    border-radius: 10px;
    font-size: 1rem;
    color: #000;
    outline: none;
    transition: border-color 0.2s, box-shadow 0.2s;
  }

  input:focus, select:focus {
    border-color: var(--accent);
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

  .restaurant-item {
    background: var(--card-bg);
    padding: 1rem;
    border-radius: var(--radius);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    margin-bottom: 1.5rem;
  }

  .restaurant-header h3 {
    margin: 0;
    color: var(--accent);
    font-size: 1.4rem;
  }

  .restaurant-content p {
    margin: 0.5rem 0;
    color: var(--text);
    font-size: 1rem;
  }

  .restaurant-actions {
    text-align: right;
    margin-top: 1rem;
  }

  .restaurant-actions button {
    background: #ff4e4e;
    border: none;
    border-radius: var(--radius);
    color: #fff;
    padding: 0.5rem 1rem;
    cursor: pointer;
    transition: background 0.2s ease;
  }

  .restaurant-actions button:hover {
    background: #ff1c1c;
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
</style>



