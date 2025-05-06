<template>
  <main class="wishlist-page">
    <div
      class="card wishlist-card"
      v-for="(wishlist, index) in paginatedWishlists"
      :key="wishlist.id || index"
    >
      <div class="wishlist-header">
        <h3>{{ wishlist.name }}</h3>
        <p>by {{ wishlist.user.first_name }} {{ wishlist.user.last_name }}</p>
        <div class="wishlist-actions">
          <button @click="viewWishlist(wishlist.id)">Share</button>
        </div>
      </div>

      <div v-if="selectedWishlist && wishlist.id === selectedWishlist.id" class="share-section">
        <label>Share with friends:</label>
        <select v-model="friendsToShare" multiple>
          <option
            v-for="friend in acceptedFriends"
            :key="friend.id"
            :value="friend.id"
          >
            {{ friend.username }}
          </option>
        </select>
        <button @click="shareWishlist(selectedWishlist.id)">Confirm</button>
      </div>
    </div>

    <!-- pagination controls -->
    <div class="pagination-controls">
      <button @click="currentPage--" :disabled="currentPage===1">Previous</button>
      <span>Page {{ currentPage }} of {{ totalPages }}</span>
      <button @click="currentPage++" :disabled="currentPage===totalPages">Next</button>
    </div>
  </main>
</template>



<script lang="ts">
  import { defineComponent } from "vue";
  import { User, Wishlist, Restaurant} from "../types/index";
  import { useUserStore } from "../stores/user";
  import { useUsersStore } from "../stores/users";
  import { useRestaurantsStore } from "../stores/restaurants";
  import { useWishlistsStore } from "../stores/wishlists";
  import { useFriendshipsStore } from "../stores/friendships";
  import VueCookies from 'vue-cookies';

  


  export default defineComponent({
      data() {
          return {
            newWishlist: {
                name: "",
              
                
            },
            wishlists: [],
            selectedWishlistItems: [],
            friendsToShare: [],
            selectedWishlist: "",
            sharedWishlists: [],
            currentPage: 1,
            perPage: 3, 

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


            // Fetching all reviews from the backend
            const resp = await fetch('http://localhost:8000/wishlists/');
            const data = await resp.json();
            this.wishlists = data.wishlists;
            this.selectedWishlistItems = data.items;  
            
            let usersResponse = await fetch("http://localhost:8000/users/");
            let usersData = await usersResponse.json();
            this.usersStore.saveUsers(usersData.users);


            let responseF = await fetch("http://localhost:8000/friendships/");
            let dataF = await responseF.json();
            let friendships = dataF.friendships;

            const friendshipsStore = useFriendshipsStore();
            friendshipsStore.saveFriendships(friendships);

            const userId = this.userStore.user.id;
            const responseS = await fetch(`http://localhost:8000/shared_wishlists/${userId}/`);
            const dataS = await responseS.json();
            this.sharedWishlists = dataS.shared_wishlists;
      },
      methods: {
        formatDate(date) {
            const d = new Date(date);
            return d.toLocaleDateString();  // This will display only the date in the format 'MM/DD/YYYY'
        },
        async viewWishlist(wishlistId: number) {
          try {
            const response = await fetch(`http://localhost:8000/wishlist/${wishlistId}/items/`);
            const data = await response.json();
   
            this.selectedWishlistItems = data.items;

            // 👇 You must store the selected wishlist
            const wishlist = this.wishlists.find(w => w.id === wishlistId);
            this.selectedWishlist = wishlist;

          } catch (error) {
            console.error("Error fetching wishlist items:", error);
            alert("Failed to load wishlist contents.");
          }
        },

        async shareWishlist(wishlistId: number) {
          const payload = {
            shared_with: this.friendsToShare, // list of user IDs
          };

          try {
            const response = await fetch(`http://localhost:8000/share_wishlist/${wishlistId}/`, {
              method: "PUT",
              headers: {
                "Authorization": `Bearer ${VueCookies.get("access_token")}`,
                "Content-Type": "application/json",
                "X-CSRFToken": VueCookies.get("csrftoken"),
              },
              credentials: "include",
              body: JSON.stringify(payload),
            });

            if (response.ok) {
              alert("Wishlist shared successfully!");
              // Optionally reload or refetch shared data
              // await this.fetchSharedWishlists();
            } else {
              const error = await response.text();
              console.error("Failed to share wishlist:", error);
              alert("Failed to share wishlist.");
            }
          } catch (err) {
            console.error("Error in shareWishlist:", err);
            alert("An error occurred while sharing the wishlist.");
          }
        },


        
          /* Creating a New review */
        async createWishlist() {
            const wishlistsStore = useWishlistsStore();
            const userId = this.userStore.user.id;
            const newWishlist = this.newWishlist;
            const payload = {
                name: this.newWishlist.name,
                owner: userId,
                
            };
            
            console.log(payload); 
            
            
            try {
              const wishlistResponse = await fetch('http://localhost:8000/wishlists/', {
                method: 'POST',
                headers: {
                  'Authorization': `Bearer ${VueCookies.get('access_token')}`,
                  'Content-Type': 'application/json',
                  'X-CSRFToken': VueCookies.get('csrftoken'),
                },
                credentials: 'include',
                body: JSON.stringify(payload),
              });

              if (!wishlistResponse.ok) {
                const errorText = await wishlistResponse.text();
                console.error("Server error response:", errorText);  // SHOW this in console
                throw new Error(errorText);
              }

              const data = await wishlistResponse.json();
              wishlistsStore.addWishlist(data.wishlist);
              window.location.reload();
              alert('Wishlist added successfully!');
            } catch (error) {
              console.error('Error creating Wishlist:', error);
              alert('Failed to create Wishlist');
            }

        },
        async deleteWishlist(wishlistId: number) {
            // Check if the logged-in user is the one who wrote the wishlist
            const wishlistToDelete = this.wishlists.find(wishlist => wishlist.id === wishlistId);
            if (!wishlistToDelete || wishlistToDelete.user.id !== this.user.id) {
                alert("You cannot delete this wishlist. Only the author can delete it.");
                return; 
            }

            try {
                const response = await fetch(`http://localhost:8000/wishlist/${wishlistId}/`, {
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
                    this.wishlists = this.wishlists.filter(wishlist => wishlist.id !== wishlistId);
                    alert('wishlist deleted successfully!');
                } else {
                    alert('Failed to delete the wishlist.');
                }
            } catch (error) {
                console.error('Error deleting wishlist:', error);
                alert('Failed to delete the wishlist.');
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
          acceptedFriends() {
            const friendshipsStore = useFriendshipsStore();
            const usersStore = useUsersStore();

            return friendshipsStore.friendships
              .filter(f => f.user === this.user.id && f.accepted)
              .map(f => usersStore.users.find(u => u.id === f.friend))
              .filter(u => u);  // remove undefined
          },
          totalPages(): number {
            return Math.ceil(this.wishlists.length / this.perPage)
          },
          paginatedWishlists(): Wishlist[] {
            const start = (this.currentPage - 1) * this.perPage
            return this.wishlists.slice(start, start + this.perPage)
          }

    
      },
      watch: {
        wishlists() {
          this.currentPage = 1
        }
      },
      setup() {
          const userStore = useUserStore();
          const wishlistsStore = useWishlistsStore();
          const restaurantsStore = useRestaurantsStore();
          const usersStore = useUsersStore();
          return { userStore , wishlistsStore , usersStore, restaurantsStore};
      },
  });
</script>



<style scoped>
:root {
  --bg-start: #0f0c29;
  --bg-end:   #302b63;
  --card-bg:  rgba(255,255,255,0.05);
  --accent:   #ff00c1;
  --text:     #eee;
  --muted:    #aaa;
  --radius:   12px;
}

.wishlist-page {
  background: linear-gradient(135deg, var(--bg-start), var(--bg-end));
  min-height: 100vh;
  padding: 2rem;
  font-family: 'Segoe UI', sans-serif;
  color: var(--text);
}

/* The “card” wrapper */
.card.wishlist-card {
  background: var(--card-bg);
  padding: 1.5rem;
  border-radius: var(--radius);
  box-shadow: 0 4px 20px rgba(0,0,0,0.4);
  margin-bottom: 2rem;
}

/* Header inside each card */
.wishlist-header h3 {
  margin: 0 0 0.5rem;
  color: var(--accent);
}
.wishlist-header p {
  color: var(--muted);
  margin: 0 0 1rem;
}

/* Buttons match the theme */
button {
  background: linear-gradient(90deg, #ff0080, #ff8c00);
  border: none;
  padding: 0.6rem 1.2rem;
  color: #fff;
  border-radius: var(--radius);
  cursor: pointer;
  transition: transform .15s ease;
}
button:hover {
  transform: scale(1.05);
}

/* Optional: spacing for your share section */
.share-section {
  margin-top: 1rem;
}

/* Pagination (if you haven’t already) */
.pagination-controls {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-top: 1rem;
}
.pagination-controls button {
  background: linear-gradient(90deg,#ff0080,#ff8c00);
  color: #fff;
  border: none;
  padding: .5rem 1rem;
  border-radius: 8px;
}
.pagination-controls button:disabled {
  opacity: .5;
  cursor: not-allowed;
}
</style>


