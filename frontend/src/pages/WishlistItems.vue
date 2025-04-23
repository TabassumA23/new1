<template>
    <div class="body">
        <div id="create-review">
            <h2>Welcome {{ user.first_name }}</h2>
      <!-- Form to Add a New review. -->
      
          <h3>Want to add a new restaurant to your wishlist ?</h3>
          <label for="wishlist">Select Wishlist:</label>
            <select id="wishlists" v-model="newWishlistItem.wishlist">
            <option v-for="wishlist in wishlists" :key="wishlist.id" :value="wishlist">
                {{ wishlist.name }}
            </option>
            </select>
          <label for="restaurant">Select Restaurant:</label>
            <select id="restaurants" v-model="newWishlistItem.restaurant">
            <option v-for="restaurant in restaurants" :key="restaurant.id" :value="restaurant">
                {{ restaurant.name }}
            </option>
            </select>
           <button type="submit" @click="createWishlistItem">Add WishlistItem</button>
     <div class="review-blog">
     <br></br>
    <div>
      <h2>All Wishlists</h2>
      <div class="wishlist-item" v-for="(wishlistItem, index,) in wishlistItems" :key="index">
          <div class="wishlist-header">
              <h3>{{ wishlistItem.wishlist }}</h3>
              <h3>{{ wishlistItem.restaurant }}</h3>
              <!-- <p>by {{ wishlist.user.first_name }} {{ wishlist.user.last_name }}</p> -->
          </div>
          <div class="wishlist-actions" v-if="wishlistItem.owner.id === user.id">
              <button @click="deleteWishlistItem(wishlistItem.id)">Delete WishlistItem</button>
          </div>
      </div>
    </div>
    </div>

  </div>
  
</div>  
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
            let responseW = await fetch(`http://localhost:8000/wishlists/`);
            let wishlistData = await responseW.json();
            

            // Update the state with the fetched restaurant data
            let madeWishlists = wishlistData.wishlists as Wishlist[];
            const wishlistsStore = useWishlistsStore();
            wishlistsStore.saveWishlists(madeWishlists); 
            console.log(responseW)

            

            // Fetching all reviews from the backend
            const resp = await fetch('http://localhost:8000/wishlistItems/');
            const data = await resp.json();
            this.wishlistItems = data.wishlistItems;  // Make sure the backend sends an array of reviews
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

            
            console.log(payload); 
            
            
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
  /* 1) Base & Variables */
  :root {
    --bg-start: #0f0c29;
    --bg-end:   #302b63;
    --card-bg:  rgba(255, 255, 255, 0.05);
    --accent:   #ff00c1;
    --text:     #eee;
    --muted:    #aaa;
    --radius:   12px;
  }
  .profile-page {
    font-family: 'Segoe UI', sans-serif;
    color: var(--text);
    background: linear-gradient(135deg, var(--bg-start), var(--bg-end));
    min-height: 100vh;
    padding: 2rem;
  }

  /* 2) Hero */
  .hero {
    display: flex; flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
  }
  .hero-content h1 {
    font-size: 2.5rem;
    margin: 0;
    letter-spacing: 1px;
  }
  .subtitle {
    color: var(--muted);
    margin-top: 0.5rem;
  }
  .hero-nav .btn {
    margin-left: 1rem;
  }

  /* 3) Grid */
  .grid-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1.5rem;
  }

  /* 4) Card */
  .card {
    background: var(--card-bg);
    padding: 1.5rem;
    border-radius: var(--radius);
    box-shadow: 0 4px 20px rgba(0,0,0,0.4);
  }
  .card h2 {
    margin-top: 0;
    border-bottom: 1px solid rgba(255,255,255,0.2);
    padding-bottom: 0.5rem;
  }

  /* 5) Profile details */
  .profile-card dl {
    display: grid;
    grid-template-columns: 1fr 2fr;
    row-gap: 0.75rem;
    column-gap: 1rem;
    margin: 1rem 0;
  }
  .profile-card dt {
    font-weight: 600;
    color: var(--muted);
  }
  .profile-card dd {
    margin: 0;
  }

  /* 6) Buttons */
  .btn,
  .btn-sm {
    background: linear-gradient(90deg, #ff0080, #ff8c00);
    border: none;
    padding: 0.65rem 1.2rem;
    color: #fff;
    font-weight: 600;
    border-radius: var(--radius);
    cursor: pointer;
    transition: transform .15s ease;
  }
  .btn:hover,
  .btn-sm:hover {
    transform: scale(1.05);
  }
  .btn-sm {
    padding: 0.4rem 0.8rem;
    font-size: 0.85rem;
  }
  .btn-outline {
    background: transparent;
    border: 2px solid var(--accent);
    color: var(--accent);
    margin-right: 0.5rem;
  }

  /* 7) Preferences tags */
  .prefs-group {
    margin: 1rem 0;
    display: flex; align-items: center;
  }
  .prefs-group label {
    flex: 0 0 70px;
  }
  .prefs-group select {
    flex: 1;
    padding: 0.5rem;
    background: rgba(255,255,255,0.1);
    border: none;
    border-radius: var(--radius);
    color: var(--text);
  }
  .tag-list {
    list-style: none;
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    padding: 0;
    margin: 0.5rem 0;
  }
  .tag-list li {
    background: rgba(255,255,255,0.15);
    padding: 0.4rem 0.7rem;
    border-radius: var(--radius);
    display: flex; align-items: center;
  }
  .tag-list .remove {
    background: transparent;
    border: none;
    color: var(--muted);
    margin-left: 0.5rem;
    cursor: pointer;
  }

  /* 8) Recommendations */
  .restaurant-item {
    background: rgba(255,255,255,0.1);
    padding: 1rem;
    border-radius: var(--radius);
    margin-bottom: 1rem;
  }
  .restaurant-item h3 {
    margin: 0 0 0.5rem;
  }
  .empty-state {
    color: var(--muted);
    font-style: italic;
    text-align: center;
    margin-top: 1rem;
  }

  /* 9) Responsive tweaks */
  @media (max-width: 600px) {
    .hero {
      flex-direction: column;
      text-align: center;
    }
    .hero-nav {
      margin-top: 1rem;
    }
  }

  /* PROFILE ROWS: text on left, button on right */
  .profile-info .field {
    display: flex;
    align-items: center;   /* vertical‑center both pieces */
    margin: 0.5rem 0;      /* vertical spacing between rows */
  }

  /* let the text take up whatever room it needs, but no more */
  .profile-info .field span {
    flex: 0 1 auto;        /* don’t grow past content, can shrink if needed */
    text-align: left;
  }

  /* shove the button to the extreme right */
  .profile-info .field button {
    flex: 0 0 auto;        /* button stays its own width */
    margin-left: auto;     /* pushes it all the way right */
  }
    .profile-info .field button {
    background: linear-gradient(90deg, #ff0080, #ff8c00);
    border: none;
    padding: 0.5rem 1rem;
    color: #fff;
    font-weight: 600;
    border-radius: var(--radius);
    cursor: pointer;
    transition: transform .15s ease;
    margin-left: auto; /* keeps them lined up on the right */
  }
  .profile-info .field button:hover {
    transform: scale(1.05);
  }
 .wishlist-page {
  font-family: 'Segoe UI', sans-serif;
  color: #eee;
  background: linear-gradient(135deg, #0f0c29, #302b63);
  min-height: 100vh;
  padding: 2rem;
 }
</style>

