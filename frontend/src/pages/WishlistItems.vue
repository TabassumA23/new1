<template>
  <main class="wishlist-page">
    <!-- Create Wishlist Item Card -->
    <div class="card wishlist-card">
      <h3>Add Restaurant to Wishlist</h3>
      <label for="wishlist-select">Select Wishlist:</label>
      <select id="wishlist-select" v-model="newWishlistItem.wishlist">
        <option v-for="wishlist in wishlists" :key="wishlist.id" :value="wishlist">{{ wishlist.name }}</option>
      </select>

      <label for="restaurant-select">Select Restaurant:</label>
      <select id="restaurant-select" v-model="newWishlistItem.restaurant">
        <option v-for="restaurant in restaurants" :key="restaurant.id" :value="restaurant"> {{ restaurant.name }}</option>
      </select>

      <button @click="createWishlistItem">Add to Wishlist</button>
    </div>
  </main>
</template>


<script lang="ts">
  import { defineComponent } from "vue";
  import { User, Wishlist,WishlistItem, Restaurant} from "../types/index";
  import { useUserStore } from "../stores/user";
  import { useUsersStore } from "../stores/users";
  import { useRestaurantsStore } from "../stores/restaurants";
  import { useWishlistsStore } from "../stores/wishlists";
  import { useWishlistItemsStore } from "../stores/wishlistItems";
  import VueCookies from 'vue-cookies';

  


  export default defineComponent({
      data() {
          return {
            newWishlistItem: {
                restaurant: "",  
                wishlist:"",
            },
            wishlistItems: [],
            currentPage: 1,
            perPage: 5
          
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
                // Fetching all restaurants from the backend
            let response = await fetch(`http://localhost:8000/restaurants/`);
            let restaurantData = await response.json();
            

            // Update the state with the fetched restaurant data
            let madeRestaurants = restaurantData.restaurants as Restaurant[];
            const restaurantsStore = useRestaurantsStore();
            restaurantsStore.saveRestaurants(madeRestaurants); 
    
                // Fetching all restaurants from the backend
            let responseW = await fetch(`http://localhost:8000/wishlists/`);
            let wishlistData = await responseW.json();
            

            // Update the state with the fetched restaurant data
            let madeWishlists = wishlistData.wishlists as Wishlist[];
            const wishlistsStore = useWishlistsStore();
            wishlistsStore.saveWishlists(madeWishlists); 
   

            

            // Fetching all reviews from the backend
            const resp = await fetch('http://localhost:8000/wishlistItems/');
            const data = await resp.json();
            this.wishlistItems = data.wishlistItems;  
      },
      methods: {
        formatDate(date) {
            const d = new Date(date);
            return d.toLocaleDateString();  // This will display only the date in the format 'MM/DD/YYYY'
        },
        
          /* Creating a New review */
        async createWishlistItem() {
            const wishlistItemsStore = useWishlistItemsStore();
            const userId = this.userStore.user.id;
            const newWishlistItem = this.newWishlistItem;
            const payload = {
              wishlist_id: this.newWishlistItem.wishlist.id,
              restaurant_id: this.newWishlistItem.restaurant.id,
              owner: this.userStore.user.id,
            };

            
            
            try {
              const wishlistItemResponse = await fetch('http://localhost:8000/wishlistItems/', {
                method: 'POST',
                headers: {
                  'Authorization': `Bearer ${VueCookies.get('access_token')}`,
                  'Content-Type': 'application/json',
                  'X-CSRFToken': VueCookies.get('csrftoken'),
                },
                credentials: 'include',
                body: JSON.stringify(payload),
              });

              if (!wishlistItemResponse.ok) {
                const errorText = await wishlistItemResponse.text();
                console.error("Server error response:", errorText);  
                throw new Error(errorText);
              }

              const data = await wishlistItemResponse.json();
              wishlistItemsStore.addWishlistItem(data.wishlistItem);
              window.location.reload();
              alert('WishlistItem added successfully!');
            } catch (error) {
              console.error('Error creating WishlistItem:', error);
              alert('Failed to create WishlistItem');
            }

        },
        async deleteWishlistItem(wishlistItemId: number) {
            // Check if the logged-in user is the one who wrote the wishlist
            const wishlistItemToDelete = this.wishlistItems.find(wishlistItem => wishlistItem.id === wishlistItemId);
            if (!wishlistItemToDelete || wishlistItemToDelete.owner.id !== this.user.id) {
                alert("You cannot delete this wishlistItem. Only the author can delete it.");
                return; 
            }

            try {
                const response = await fetch(`http://localhost:8000/wishlistItem/${wishlistItemId}/`, {
                    method: 'DELETE',
                    headers: {
                        'Authorization': `Bearer ${VueCookies.get('access_token')}`,
                        'Content-Type': 'application/json',
                        'X-CSRFToken': VueCookies.get('csrftoken'),
                    },
                    credentials: 'include',
                });

                if (response.ok) {
                    // Remove the deleted review from the list
                    this.wishlistItems = this.wishlistItems.filter(wishlistItem => wishlistItem.id !== wishlistItemId);
                    alert('wishlistItem deleted successfully!');
                } else {
                    alert('Failed to delete the wishlistItem.');
                }
            } catch (error) {
                console.error('Error deleting wishlistItem:', error);
                alert('Failed to delete the wishlistItem.');
            }
        },

      }, 
      computed: {
          user() {
              const userStore = useUserStore;
              return this.userStore.user; // Bind to the fetched user data from Pinia store
          },
          wishlists(): Wishlist[]{
              const wishlistsStore = useWishlistsStore;
              return this.wishlistsStore.wishlists; // Bind to the fetched cuisine data from Pinia store
          },
          restaurants(): Restaurant[]{
              const restaurantsStore = useRestaurantsStore;
              return this.restaurantsStore.restaurants; // Bind to the fetched cuisine data from Pinia store
          },
          wishlistItems(): WishlistItem[]{
              const wishlistItemsStore = useWishlistItemsStore;
              return this.wishlistItemsStore.wishlistItems; // Bind to the fetched cuisine data from Pinia store
          },
          totalPages() {
            return Math.ceil(this.wishlistItems.length / this.perPage) || 1;
          },
          paginatedItems() {
            const start = (this.currentPage - 1) * this.perPage;
            return this.wishlistItems.slice(start, start + this.perPage);
          }
      },
      setup() {
          const userStore = useUserStore();
          const wishlistsStore = useWishlistsStore();
          const restaurantsStore = useRestaurantsStore();
          const usersStore = useUsersStore();
          const wishlistItemsStore = useWishlistItemsStore();
          return { userStore , wishlistsStore , usersStore, restaurantsStore, wishlistItemsStore};
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

  .wishlist-page {
    background: linear-gradient(135deg, var(--bg-start), var(--bg-end));
    min-height: 100vh;
    padding: 2rem;
    font-family: 'Segoe UI', sans-serif;
    color: var(--text);
  }

  .card.wishlist-card {
    background: var(--card-bg);
    padding: 1.5rem;
    border-radius: var(--radius);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    margin-bottom: 2rem;
  }

  h2, h3 {
    margin-bottom: 1rem;
    color: var(--text);
  }

  label, select, button {
    display: block;
    width: 100%;
    margin-bottom: 1rem;
  }

  select {
    padding: 0.75rem;
    background: rgba(255, 255, 255, 0.07);
    border: 2px solid #ff8c00;
    border-radius: 10px;
    font-size: 1rem;
    color: #000;
    outline: none;
    transition: border-color 0.2s ease;
  }

  select:focus {
    border-color: var(--accent);
    box-shadow: 0 0 0 3px rgba(255, 0, 193, 0.2);
  }

  button {
    background: linear-gradient(90deg, #ff0080, #ff8c00);
    border: none;
    padding: 0.75rem;
    color: #fff;
    font-weight: 600;
    border-radius: var(--radius);
    cursor: pointer;
    transition: transform 0.15s ease;
  }

  button:hover {
    transform: scale(1.05);
  }

  .wishlist-item {
    background: var(--card-bg);
    padding: 1rem;
    border-radius: var(--radius);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    margin-bottom: 1rem;
  }

  .wishlist-header h3 {
    margin: 0;
    color: var(--accent);
  }

  .wishlist-header p {
    margin: 0.5rem 0 0;
    color: var(--muted);
  }

  .wishlist-actions {
    text-align: right;
    margin-top: 1rem;
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

