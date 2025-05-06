<template>
  <main class="restaurant-page">
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
      <div class="restaurant-item" v-for="(restaurant, index) in paginatedRestaurants" :key="restaurant.id || index">
        <div class="restaurant-header">
          <h3>{{ restaurant.name }}</h3>
        </div>
        <div class="restaurant-content">
          <p><strong>Cuisine:</strong> {{ restaurant.cuisine }}</p>
          <p><strong>Allergies:</strong> 
            <span v-for="a in allergys" :key="a.id" :value="a.id">
              {{ a.name }} |
            </span>
          </p>
          <p><strong>Rating:</strong> {{ restaurant.rating }}</p>
          <p><strong>Seats:</strong> {{ restaurant.seats_available }}</p>
          <p><strong>Location:</strong> {{ restaurant.location }}</p>
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
  import { useCookies } from 'vue3-cookies';  

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
          };
      },
      async mounted() {
          // Fetching csrf token using session cookie information on mount
          const sessionCookie = (document.cookie).split(';');
          let currentSessionid: string = ''
 
          // Checking in UserStore with CSRF token
          for (let cookie of sessionCookie) {
              cookie = cookie.trim();

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

              } catch (error) {
                  console.error("Error fetching user:", error);
              }
          

          }
          else{
              // Extracting user id from url query
              const params = new URLSearchParams(window.location.search);
              const userId: number = parseInt(params.get("u") || "0");
      
              // Fetch user data using url query information on mount
              let user = await this.userStore.fetchUserReturn(userId);
          
              this.userStore.user = user;
              // Set session variable
              sessionStorage.setItem("user_id", userId.toString());
              
              // Fetching csrf token using session cookie information on mount
              const session_cookie = (document.cookie).split(';');
   

              //Update user state in UserStore with CSRF token
              for (let cookie of session_cookie) {
                  cookie = cookie.trim();
      
                  if (cookie.startsWith("csrftoken" + "=")) {
                      this.userStore.setCsrfToken(cookie.substring("csrftoken".length + 1));

                  }
                  //Update sessionStorage state in UserStore with CSRF token
         
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
          

          // Fetching all allergys from the backend
          let responseC = await fetch(`http://localhost:8000/allergys/`);
          let allergyData = await responseC.json();
        

          // Update the state with the fetched restaurant data
          let madeAllergys = allergyData.allergys as Allergy[];
          const allergysStore = useAllergysStore();
          allergysStore.saveAllergys(madeAllergys); 
    

          //fetch all the friendships
          let responseChosen = await fetch("http://localhost:8000/chosens/");
          let dataChosen = await responseChosen.json();
          let chosens = dataChosen.chosens as Chosen[];
  
          const storeChosens = useChosensStore();
          storeChosens.saveChosens(chosens);

          // Fetching all restaurants from the backend
          let responseR = await fetch(`http://localhost:8000/restaurants/`);
          let restaurantData = await responseR.json();
        

          // Update the state with the fetched restaurant data
          let madeRestaurants = restaurantData.restaurants as Restaurant[];
          const restaurantsStore = useRestaurantsStore();
          restaurantsStore.saveRestaurants(madeRestaurants); 
      

      },
      methods: {
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
            const { cookies } = useCookies();
            const payload = {
                [field.toLowerCase()]: this.editedUser[field.toLowerCase()],
            };
        
            const response = await fetch(`http://localhost:8000/user/${this.user.id}/`, {
              method: "PUT",
              headers: {
                'Authorization': `Bearer ${cookies.get('access_token')}`,
                'Content-Type': 'application/json',
                'X-CSRFToken': cookies.get('csrftoken'),
              },
              credentials: 'include',
              body: JSON.stringify(payload),
            });       
         
            if (!response.ok) {
              throw new Error("Failed to update field");
            }
            const updatedUser = await response.json();
       
       
            this.userStore = this.userStore.saveUsers(updatedUser); // Update the user state in the store
            window.location.reload();
            alert(`${field} updated successfully!`);
          } catch (error) {
            console.error(error);
            alert(`Failed to update ${field}.`);
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



