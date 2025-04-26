<template>
  <main class="wishlist-page">
    <div class="card wishlist-card">
      <!-- <h2>Welcome {{ user.first_name }}</h2> -->
      <h3>Create a New Wishlist</h3>
      <label for="wishlist">Title for Wishlist:</label>
      <textarea
        id="name"
        v-model="newWishlist.name"
        required
        rows="2"
        cols="50"
        placeholder="Type wishlist name here..."
      ></textarea>
      <button @click="createWishlist">Add Wishlist</button>

      <div class="btn-group">
        <RouterLink to="/wishlistItems" class="btn">Add content to wishlist</RouterLink>
        <RouterLink to="/shares" class="btn">Share wishlist with a friend</RouterLink>
      </div>
    </div>
    
    <h2>All your wishlists</h2>
    <div class="card wishlist-card">
      <div class="wishlist-item" v-for="(wishlist, index) in paginatedWishlists" :key="index">
        <div class="wishlist-header">
          <h3>{{ wishlist.name }}</h3>
          <p>by {{ wishlist.user.first_name }} {{ wishlist.user.last_name }}</p>

          <div v-if="selectedWishlist && wishlist.id === selectedWishlist.id">
            <h4>Wishlist Contents:</h4>
            <ul>
              <li v-for="item in selectedWishlistItems" :key="item.id">
                {{ item.restaurant }}
              </li>
            </ul>
          </div>

          <div class="wishlist-actions">
            <button @click="viewWishlist(wishlist.id)">View Wishlist</button>
            <button v-if="wishlist.user.id === user.id" @click="deleteWishlist(wishlist.id)">Delete Wishlist</button>
          </div>
        </div>
      </div>
    </div>
    <div class="pagination-controls">
      <button @click="currentPage--" :disabled="currentPage === 1">Previous</button>
      <span>Page {{ currentPage }} of {{ totalPages }}</span>
      <button @click="currentPage++" :disabled="currentPage === totalPages">Next</button>
    </div>

    <h2>Wishlists Shared With Me</h2>
    <div class="card wishlist-card">
      <div v-for="wishlist in paginatedSharedWishlists" :key="wishlist.id">
        <h3>{{ wishlist.name }}</h3>
        <p>Owner: {{ wishlist.user.first_name }} {{ wishlist.user.last_name }}</p>
      </div>
    </div>
    <div class="pagination-controls">
      <button @click="currentSharedPage--" :disabled="currentSharedPage === 1">Previous</button>
      <span>Page {{ currentSharedPage }} of {{ totalSharedPages }}</span>
      <button @click="currentSharedPage++" :disabled="currentSharedPage === totalSharedPages">Next</button>
    </div>


  </main>
</template>


<script lang="ts">
  import { defineComponent } from "vue";
  import { User, Wishlist, Friendship} from "../types/index";
  import { useUserStore } from "../stores/user";
  import { useUsersStore } from "../stores/users";
  import { useFriendshipsStore } from "../stores/friendships";
  import { useWishlistsStore } from "../stores/wishlists";
  import { useCookies } from 'vue3-cookies';

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
        itemsPerPage: 3, 
        currentSharedPage: 1,
        sharedPerPage: 4,

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
      async viewWishlist(wishlistId: number) {
        try {
          const response = await fetch(`http://localhost:8000/wishlist/${wishlistId}/items/`);
          const data = await response.json();
          console.log("Wishlist contents:", data.items);
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
            const { cookies } = useCookies();
          const response = await fetch(`http://localhost:8000/share_wishlist/${wishlistId}/`, {
            method: "PUT",
            headers: {
              "Authorization": `Bearer ${cookies.get("access_token")}`,
              "Content-Type": "application/json",
              "X-CSRFToken": cookies.get("csrftoken"),
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
          const newName = this.newWishlist.name.trim();

          const duplicate = this.wishlists.some(w => w.name.toLowerCase() === newName.toLowerCase() && w.user.id === userId);
          if (duplicate) {
            alert("You already have a wishlist with that name. Please choose a different name.");
            return;
          }
          const payload = {
              name: newName,
              owner: userId,
              
          };
          
          console.log(payload); 
          
          
          try {
              const { cookies } = useCookies();
            const wishlistResponse = await fetch('http://localhost:8000/wishlists/', {
              method: 'POST',
              headers: {
                'Authorization': `Bearer ${cookies.get('access_token')}`,
                'Content-Type': 'application/json',
                'X-CSRFToken': cookies.get('csrftoken'),
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
              const { cookies } = useCookies();
              const response = await fetch(`http://localhost:8000/wishlist/${wishlistId}/`, {
                  method: 'DELETE',
                  headers: {
                      'Authorization': `Bearer ${cookies.get('access_token')}`,
                      'Content-Type': 'application/json',
                      'X-CSRFToken': cookies.get('csrftoken'),
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
        user(): User | undefined {
            const userStore = useUserStore();
            return userStore.user;
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
            .filter(u => u);  
        },
        paginatedWishlists() {
          const start = (this.currentPage - 1) * this.itemsPerPage;
          const end = start + this.itemsPerPage;
          return this.wishlists.slice(start, end);
        },
        totalPages() {
          return Math.ceil(this.wishlists.length / this.itemsPerPage);
        },
        paginatedSharedWishlists() {
          const start = (this.currentSharedPage - 1) * this.sharedPerPage;
          const end = start + this.sharedPerPage;
          return this.sharedWishlists.slice(start, end);
        },
        totalSharedPages() {
          return Math.ceil(this.sharedWishlists.length / this.sharedPerPage);
        }

  
    },
    setup() {
        const userStore = useUserStore();
        const wishlistsStore = useWishlistsStore();
        const usersStore = useUsersStore();
        return { userStore , wishlistsStore , usersStore};
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
    font-family: 'Segoe UI', sans-serif;
    color: var(--text);
    padding: 2rem;
  }

  .card {
    background: var(--card-bg);
    padding: 1.5rem;
    border-radius: var(--radius);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    margin-bottom: 2rem;
  }

  textarea,
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

  textarea:focus,
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
  }

  button:hover {
    transform: scale(1.05);
  }

  .btn-group {
    display: flex;
    gap: 1rem;
    margin-top: 1rem;
  }

  ul {
    list-style: none;
    padding: 0;
  }

  li {
    background: rgba(255, 255, 255, 0.1);
    margin: 0.5rem 0;
    padding: 0.75rem;
    border-radius: var(--radius);
  }

  h2, h3, h4 {
    margin-bottom: 1rem;
    color: var(--text);
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
