<template>
    <div class="body">
        <div id="profile-box">
            <h2>Welcome {{ user.first_name }}</h2>
           
    
    <!-- <div class="review">
    <label for="reviews">Choose a review:</label>
    <select id="reviews" v-model="chosenReview">
        <option v-for="review in reviews" :key="review.id">
            {{ review.name }}: {{ review.review }}
        </option>
    </select>
    <button @click="addReviewChoice">Save Review Choice Here</button>
    
    <div class="reviews">
        <h4>Reviews</h4>
        <ul v-for="(review, index) in reviews" :key="index">
            <li class="review-item" v-if="review.user == user.id">
                {{ review.name }}: {{ review.review }} 
                <button @click="deleteReview(review.id)"> Delete </button>
            </li>
        </ul>
    </div>
    </div> -->


      <!-- Form to Add a New review. -->
      <div id="create-review">
          <h3>Want to add a new review to this website?</h3>
          <h6>Double check spelling before submission!!</h6>
          <label for="name">Name of Review:</label><br>
          <input id="name" v-model="newReview.name" type="text" required=true class="form-control"/><br>
          <label for="review">Brief review Description:</label><br>
        <textarea id="description" v-model="newReview.description" required class="form-control" rows="2" cols="50"></textarea><br>

          <button type="submit" @click="createReview">Add Review</button>
      </div>
  </div>
     <div class="review-blog">
            <h2>All Reviews</h2>

    <div class="review-item" v-for="(review, index,) in reviews" :key="index">
        <div class="review-header">
            <h3>{{ review.name }}</h3> <!-- Title of the review -->
           <p><strong>By:</strong> {{ review.user.id }} {{ review.user.first_name }} {{ review.user.last_name }} | <strong>Date:</strong> {{ formatDate(review.date) }}</p>

        </div>
        
        <div class="review-content">
            <p>{{ review.description }}</p> <!-- Review content -->
        </div>
        
        <div class="review-actions" v-if="review.user.id === user.id">
            <button @click="deleteReview(review.id)">Delete Review</button>
        </div>
    </div>

    </div>

  </div>
  
  
</template>

<script lang="ts">
  import { defineComponent } from "vue";
  import { User, Review} from "../types/index";
  import { useUserStore } from "../stores/user";
  import { useUsersStore } from "../stores/users";
  import { useReviewsStore } from "../stores/reviews";
  import VueCookies from 'vue-cookies';

  


  export default defineComponent({
      data() {
          return {
          newReview: {
              name: "",
              description: "",
              
          },
          reviews: [],  // Store for reviews fetched from the backend
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
            const response = await fetch('http://localhost:8000/reviews/');
            const data = await response.json();
            this.reviews = data.reviews;  // Make sure the backend sends an array of reviews
      },
      methods: {
        formatDate(date) {
            const d = new Date(date);
            return d.toLocaleDateString();  // This will display only the date in the format 'MM/DD/YYYY'
        },
        
          /* Creating a New review */
        async createReview() {
            const reviewsStore = useReviewsStore();
            const userId = this.userStore.user.id;
            const newReview = this.newReview;
            const payload = {
                name: this.newReview.name,
                description: this.newReview.description,  
                user_id: userId,
            };
            
            console.log(payload); 
            console.log(userId);  
            

            const reviewResponse = await fetch('http://localhost:8000/reviews/', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${VueCookies.get('access_token')}`,
                    'Content-Type': 'application/json',
                    'X-CSRFToken': VueCookies.get('csrftoken'),
                },
                credentials: 'include',
                body: JSON.stringify(payload),
            });

            const responseText = await reviewResponse.text();  // Log raw response for debugging
            console.log(responseText);

            // Add the newly created review to the Pinia store
            // const data = await reviewResponse.json();
            // let createdReview = data.review;
            // reviewsStore.addReview(createdReview);
            window.location.reload();
            alert('Review added successfully!');
        },
        async deleteReview(reviewId: number) {
            // Check if the logged-in user is the one who wrote the review
            const reviewToDelete = this.reviews.find(review => review.id === reviewId);
            if (!reviewToDelete || reviewToDelete.user.id !== this.user.id) {
                alert("You cannot delete this review. Only the author can delete it.");
                return; // Prevent deletion
            }

            try {
                const response = await fetch(`http://localhost:8000/review/${reviewId}/`, {
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
                    this.reviews = this.reviews.filter(review => review.id !== reviewId);
                    alert('Review deleted successfully!');
                } else {
                    alert('Failed to delete the review.');
                }
            } catch (error) {
                console.error('Error deleting review:', error);
                alert('Failed to delete the review.');
            }
        },

      }, 
      computed: {
          user() {
              const userStore = useUserStore;
              return this.userStore.user; // Bind to the fetched user data from Pinia store
          },
          reviews(): Review[]{
              const reviewsStore = useReviewsStore;
              return this.reviewsStore.reviews; // Bind to the fetched cuisine data from Pinia store
          },
    
      },
      setup() {
          const userStore = useUserStore();
          const reviewsStore = useReviewsStore();
          const usersStore = useUsersStore();
          return { userStore , reviewsStore , usersStore};
      },
  });
</script>


<style scoped>
    /* 1) Color variables */
    :root {
    --bg-start: #0f0c29;
    --bg-end:   #302b63;
    --card-bg:  rgba(255, 255, 255, 0.05);
    --accent:   #ff00c1;
    --text:     #eee;
    --muted:    #aaa;
    --radius:   12px;
    }

    /* 2) Page background & grid */
    .body {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
    min-height: 100vh;
    padding: 2rem;
    background: linear-gradient(135deg, var(--bg-start), var(--bg-end));
    font-family: 'Segoe UI', sans-serif;
    color: var(--text);
    }

    /* 3) Profile box card */
    #profile-box {
    background: var(--card-bg);
    border-radius: var(--radius);
    box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    padding: 1.5rem;
    }

    /* 4) Create‑review card */
    #create-review {
    background: var(--card-bg);
    border-radius: var(--radius);
    box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    }

    /* 5) Review‑blog card */
    .review-blog {
    grid-column: 1 / span 2;
    background: var(--card-bg);
    border-radius: var(--radius);
    box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    padding: 1.5rem;
    }

    /* 6) Headings */
    #profile-box h2,
    #create-review h3,
    .review-blog h2 {
    margin-top: 0;
    border-bottom: 1px solid rgba(255,255,255,0.2);
    padding-bottom: 0.5rem;
    color: var(--text);
    }

    /* 7) Form inputs */
    #create-review input,
    #create-review textarea,
    #create-review select {
    width: 100%;
    padding: 0.6rem 0.8rem;
    background: rgba(255,255,255,0.1);
    border: none;
    border-radius: var(--radius);
    color: var(--text);
    }

    /* 8) Buttons & links */
    button,
    a {
    background: linear-gradient(90deg, #ff0080, #ff8c00);
    border: none;
    padding: 0.6rem 1.2rem;
    color: #fff;
    font-weight: 600;
    border-radius: var(--radius);
    cursor: pointer;
    text-decoration: none;
    display: inline-block;
    transition: transform .15s ease;
    }

    button:hover,
    a:hover {
    transform: scale(1.05);
    }

    /* 9) Review items */
    .review-item {
    background: rgba(255,255,255,0.1);
    padding: 1rem;
    border-radius: var(--radius);
    margin-bottom: 1rem;
    }

    .review-header {
    margin-bottom: 0.75rem;
    }

    .review-header h3 {
    margin: 0;
    color: var(--accent);
    }

    .review-header p {
    color: var(--muted);
    font-size: 0.9rem;
    margin: 0.25rem 0 0;
    }

    .review-content {
    color: var(--text);
    line-height: 1.5;
    }

    /* 10) Review‑actions */
    .review-actions {
    text-align: right;
    }

    .review-actions button {
    background: #ff4e4e;
    padding: 0.4rem 1rem;
    font-size: 0.85rem;
    }

    .review-actions button:hover {
    background: #ff1c1c;
    }

    /* 11) Responsive: stack on small */
    @media (max-width: 800px) {
    .body {
        grid-template-columns: 1fr;
    }
    .review-blog {
        grid-column: 1;
    }
    }
</style>

