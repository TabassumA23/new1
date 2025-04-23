<template>
    <div class="body">

    
      <div id="create-review">
          <h2>Welcome {{ user.first_name }}</h2>
          <!-- Form to Add a New review. -->
            <div>
        
          <h3>Want to add a new wishlist to this website?</h3>
          <h6>Double check spelling before submission!!</h6>
          <label for="wishlist">Title for Wishlist:</label><br>
            <textarea id="name" v-model="newWishlist.name" required class="form-control" rows="2" cols="50"></textarea><br>

          <button type="submit" @click="createWishlist">Add Wishlist</button>
      </div>
        <nav class="hero-nav">
          <RouterLink to="/shares" class="btn">Share wishlist with a friend</RouterLink>
        </nav>
      </div>
      <div>
      <nav class="hero-nav">
        <RouterLink to="/wishlistItems" class="btn">Add content to wishlist</RouterLink> 
      </nav>
    </div>
        
     <div class="review-blog">
      

    </div>
    

    
    <div class="wishlist-item" v-for="(wishlist, index) in wishlists" :key="index">
      <div class="wishlist-header">
        <h3>{{ wishlist.name }}</h3>
        <p>by {{ wishlist.user.first_name }} {{ wishlist.user.last_name }}</p>
        <!-- Only show contents for the selected wishlist -->
        <div v-if="selectedWishlist && wishlist.id === selectedWishlist.id">
          <h3>Wishlist Contents:</h3>
          <ul>
            <li v-for="item in selectedWishlistItems" :key="item.id">
              {{ item.restaurant }}
            </li>
          </ul>
        </div>

        <div class="wishlist-actions">
          <button @click="viewWishlist(wishlist.id)">View Wishlist</button>
        </div>
        <div class="wishlist-actions" v-if="wishlist.user.id === user.id">
          <button @click="deleteWishlist(wishlist.id)">Delete Wishlist</button>
        </div>
      </div>
    
        
      
    </div>


      
      

      <h2>Wishlists Shared With Me</h2>
      <div v-for="wishlist in sharedWishlists" :key="wishlist.id">
        <h3>{{ wishlist.name }}</h3>
        <p>Owner: {{ wishlist.user.first_name }} {{ wishlist.user.last_name }}</p>
      </div>


  </div>
  
  
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
            sharedWishlists: []

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
  

  .body {
  background: linear-gradient(135deg,   #302b63;, #302b63);
  padding: 2rem;
  min-height: 100vh;
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

  .wishlist-card {
    background: rgba(255, 255, 255, 0.05);
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    margin-bottom: 2rem;
  }

  input {
    width: 100%;
    padding: 1rem;
    border-radius: 10px;
    border: none;
    margin-bottom: 1rem;
    font-size: 1rem;
  }

  button {
    background: linear-gradient(90deg, #ff0080, #ff8c00);
    border: none;
    padding: 0.75rem 1.5rem;
    color: #fff;
    font-weight: 600;
    border-radius: 10px;
    cursor: pointer;
  }

  button:hover {
    transform: scale(1.05);
  }

  .wishlist-list {
    background: rgba(255, 255, 255, 0.05);
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.4);
  }

  ul {
    list-style: none;
    padding: 0;
  }

  li {
    background: rgba(255,255,255,0.1);
    margin: 0.5rem 0;
    padding: 0.75rem;
    border-radius: 10px;
  }

  span {
    font-size: 0.85rem;
    color: #aaa;
    margin-left: 1rem;
  }
</style>

