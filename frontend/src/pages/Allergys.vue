<template>
  <main class="cuisine-page">
    <div class="card form-card">
      <h3>Create a New Diatary requirement</h3>
      <textarea v-model="newAllergy.name" placeholder="Name…" rows="1"/>
      <textarea v-model="newAllergy.description" placeholder="Description…" rows="3"/>
      <button @click="createAllergy">Add </button>
    </div>
  </main>
</template>


<script lang="ts">
  import { defineComponent } from "vue";
  import { User, Allergy} from "../types/index";
  import { useUserStore } from "../stores/user";
  import { useUsersStore } from "../stores/users";
  
  import { useAllergysStore } from "../stores/allergys";
  import VueCookies from 'vue-cookies';

  


  export default defineComponent({
      data() {
        return {
            newAllergy: { name: "", description: "" }, 
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
           
            },
      methods: {
    
        
          /* Creating a New cuisine */
        async createAllergy() {
            const allergysStore = useAllergysStore();
            const userId = this.userStore.user.id;
            const rawName = this.newAllergy.name.trim();

            // 1) Reject blank
            if (!rawName) {
                return alert("Allergy name can’t be empty!");
            }

            // 2) Case-insensitive duplicate check
            const lc = rawName.toLowerCase();
            if (allergysStore.allergys.some(c => c.name.toLowerCase() === lc)) {
                return alert("You already have a match with that name.");
            }
            
            const payload = {
                name: this.newAllergy.name,
                description: this.newAllergy.description,  
                user_id: userId,
            };
            
            console.log(payload); 
            console.log(userId);  
            
            try {
                const cuisineResponse = await fetch('http://localhost:8000/allergys/', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${VueCookies.get('access_token')}`,
                        'Content-Type': 'application/json',
                        'X-CSRFToken': VueCookies.get('csrftoken'),
                    },
                    credentials: 'include',
                    body: JSON.stringify(payload),
                });

                const responseText = await cuisineResponse.text();  // Log raw response for debugging
                console.log(responseText);
                window.location.reload();
                alert('item added successfully!');
            } catch (error) {
                    console.error('Error creating item:', error);
                    alert('Failed to create item');
            }
        },
        

      }, 
      computed: {
        user() {
            const userStore = useUserStore;
            return this.userStore.user; // Bind to the fetched user data from Pinia store
        },
        allergys(): Allergy[]{
            const allergysStore = useAllergysStore;
            return this.allergysStore.allergys; // Bind to the fetched cuisine data from Pinia store
        },
        
    
      },
      setup() {
          const userStore = useUserStore();
          const allergysStore = useAllergysStore();
         
          const usersStore = useUsersStore();
          return { userStore , allergysStore , usersStore};
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
