<template>
  <main class="cuisine-page">
    <div class="card form-card">
      <h3>Create a New Cuisine</h3>
      <textarea v-model="newCuisine.name" placeholder="Name…" rows="1"/>
      <textarea v-model="newCuisine.description" placeholder="Description…" rows="3"/>
      <button @click="createCuisine">Add Cuisine</button>
    </div>
  </main>
</template>


<script lang="ts">
  import { defineComponent } from "vue";
  import { User, Cuisine, Restaurant} from "../types/index";
  import { useUserStore } from "../stores/user";
  import { useUsersStore } from "../stores/users";
  import { useRestaurantsStore } from "../stores/restaurants";
  import { useCuisinesStore } from "../stores/cuisines";
  import VueCookies from 'vue-cookies';

  


  export default defineComponent({
      data() {
        return {
            newCuisine: { name: "", description: "" }, 
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
                  console.log("Fetched User:", userCookie);
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

                      console.log(this.userStore.csrf)
                  }
                  //Update sessionStorage state in UserStore with CSRF token
         
                  if (cookie.startsWith("sessionid" + "=")) {
                     // Set session variable
                     let sessionId = cookie.substring("csrftoken".length + 1);
                     sessionStorage.setItem("session_id", sessionId);
                  }
              }
          }
           
            },
      methods: {
    
        
          /* Creating a New cuisine */
        async createCuisine() {
            const cuisinesStore = useCuisinesStore();
            const userId = this.userStore.user.id;
            const rawName = this.newCuisine.name.trim();

            // 1) Reject blank
            if (!rawName) {
                return alert("Cuisine name can’t be empty!");
            }

            // 2) Case-insensitive duplicate check
            const lc = rawName.toLowerCase();
            if (cuisinesStore.cuisines.some(c => c.name.toLowerCase() === lc)) {
                return alert("You already have a cuisine with that name.");
            }
            
            const payload = {
                name: this.newCuisine.name,
                description: this.newCuisine.description,  
                user_id: userId,
            };

            
            try {
                const cuisineResponse = await fetch('http://localhost:8000/cuisines/', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${VueCookies.get('access_token')}`,
                        'Content-Type': 'application/json',
                        'X-CSRFToken': VueCookies.get('csrftoken'),
                    },
                    credentials: 'include',
                    body: JSON.stringify(payload),
                });

       
                window.location.reload();
                alert('cuisine added successfully!');
            } catch (error) {
                    console.error('Error creating cuisine:', error);
                    alert('Failed to create cuisine');
            }
        },
        

      }, 
      computed: {
        user() {
            const userStore = useUserStore;
            return this.userStore.user; // Bind to the fetched user data from Pinia store
        },
        cuisines(): Cuisine[]{
            const cuisinesStore = useCuisinesStore;
            return this.cuisinesStore.cuisines; // Bind to the fetched cuisine data from Pinia store
        },
        
    
      },
      setup() {
          const userStore = useUserStore();
          const cuisinesStore = useCuisinesStore();
         
          const usersStore = useUsersStore();
          return { userStore , cuisinesStore , usersStore};
      },
  });
</script>


<style scoped>
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

  :root {
    --bg-start: #0f0c29;
    --bg-end: #302b63;
    --card-bg: rgba(255, 255, 255, 0.05);
    --accent: #ff00c1;
    --text: #eee;
    --muted: #aaa;
    --radius: 12px;
  }

  .cuisine-page {
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
    box-sizing: border-box;
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

  .cuisine-header h3 {
    margin: 0;
    color: var(--accent);
  }

  .cuisine-header p {
    margin: 0.25rem 0 1rem;
    font-size: 0.9rem;
    color: var(--muted);
  }

  .cuisine-content {
    color: var(--text);
    line-height: 1.5;
    margin-bottom: 1rem;
  }

  .cuisine-actions {
    text-align: right;
  }

  .cuisine-actions button {
    background: #ff4e4e;
    padding: 0.4rem 1rem;
    font-size: 0.85rem;
  }

  .cuisine-actions button:hover {
    background: #ff1c1c;
  }

  @media (max-width: 800px) {
    .cuisine-page {
      padding: 1rem;
    }
  }
</style>
