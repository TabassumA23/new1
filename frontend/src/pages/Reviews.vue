<template>
  <main class="review-page">
    <div class="card form-card">
        <h3>Create a New Review</h3>
        <label for="name">Title for Review:</label>
        <textarea id="name" v-model="newReview.name" placeholder="Give your review a name..." rows="2"></textarea>

        <label for="restaurant">Select Restaurant:</label>
        <select id="restaurants" v-model="newReview.restaurant">
        <option v-for="restaurant in restaurants" :key="restaurant.id" :value="restaurant">
            {{ restaurant.name }}
        </option>
        </select>

        <label for="rating">Overall experience rating:</label>
        <input type="number" min="1" max="5" v-model="newReview.rating" placeholder="Enter a number from 1 to 5" />
        <label for="rating">Food Rating:</label>
        <input type="number" min="1" max="5" v-model="newReview.food_rating" placeholder="Enter a number from 1 to 5" />
        <label for="rating">Service Rating:</label>
        <input type="number" min="1" max="5" v-model="newReview.service_rating" placeholder="Enter a number from 1 to 5" />
        <label for="rating">Ambience Rating:</label>
        <input type="number" min="1" max="5" v-model="newReview.ambience_rating" placeholder="Enter a number from 1 to 5" />

        <label for="description">Brief Description:</label>
        <textarea id="description" v-model="newReview.description" placeholder="What did you think?..." rows="4"></textarea>

        <button @click="createReview">Add Review</button>
    </div>

    <h2>All Reviews</h2>
    <!-- Filter by restaurant -->
      <input
        type="text"
        v-model="searchRestaurant"
        placeholder="Filter by restaurant name..."
      />
    <div class="card review-list-card">

      

      <!-- Review -->
      <div
        v-for="(review, id) in paginatedReviews"
        :key="id"
        class="review-item"
      >
        <!-- EDIT MODE -->
        <template v-if="review.user && user && review.user.id === user.id && editingId === review.id">

          <div class="review-edit-form">
            <input v-model="editedReview.name" placeholder="Review title" />
            <select v-model="editedReview.restaurantId">
              <option
                v-for="r in restaurants"
                :key="r.id"
                :value="r.id"
              >{{ r.name }}</option>
            </select>
            <input type="number" min="1" max="5" v-model="editedReview.rating" placeholder="Overall" />
            <input type="number" min="1" max="5" v-model="editedReview.food_rating" placeholder="Food" />
            <input type="number" min="1" max="5" v-model="editedReview.service_rating" placeholder="Service" />
            <input type="number" min="1" max="5" v-model="editedReview.ambience_rating" placeholder="Ambience" />
            <textarea v-model="editedReview.description" rows="3" placeholder="Description"></textarea>
            <button @click="saveReviewEdit(review.id)">Save</button>
            <button @click="cancelReviewEdit()">Cancel</button>
          </div>
        </template>

        <!-- READ-ONLY MODE -->
        <template v-else>
          <div class="review-header">
            <h3>Title: {{ review.name }}</h3>
            <p><strong>Restaurant:</strong> {{ review.restaurant?.name || 'Unknown' }}</p>
            <p>
              <strong>By:</strong>
              {{ review.user.first_name }} {{ review.user.last_name }}
              |
              <strong>Date:</strong>
              {{ formatDate(review.date) }}
            </p>
          </div>
          <div class="review-content">
            <p>Review: {{ review.description }}</p>
            <p>
              <strong>Overall:</strong> {{ review.rating }} ☆
              <strong>Food:</strong> {{ review.food_rating }} ☆
              <strong>Service:</strong> {{ review.service_rating }} ☆
              <strong>Ambience:</strong> {{ review.ambience_rating }} ☆
            </p>
            

          </div>

          <div class="review-actions" v-if="review.user && user && review.user.id === user.id">

            <button @click="startReviewEdit(review)">Edit</button>
            <button @click="deleteReview(review.id)">Delete</button>
          </div>
        </template>
      </div>

      <!-- Pagination -->
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
  import { User, Review, Restaurant} from "../types/index";
  import { useUserStore } from "../stores/user";
  import { useUsersStore } from "../stores/users";
  import { useRestaurantsStore } from "../stores/restaurants";
  import { useReviewsStore } from "../stores/reviews";
  import VueCookies from 'vue-cookies';

  


  export default defineComponent({
      data() {
        return {
            reviews: [],
            searchRestaurant: "",
            currentPage: 1,
            itemsPerPage: 4,
            newReview: {
            name: "",
            restaurant: null,
            rating: "",
            description: ""
            },

     
      editingId: null as number | null,
      editedReview: {
        name: '',
        restaurantId: 0,
        rating: 1,
        food_rating: 1,
        service_rating: 1,
        ambience_rating: 1,
        description: ''
      },

      newReview: {
        name: '',
        restaurant: null as Restaurant | null,
        rating: 1,
        food_rating: 1,
        service_rating: 1,
        ambience_rating: 1,
        description: ''
      }
    
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
            const resp = await fetch('http://localhost:8000/reviews/');
            const data = await resp.json();
            this.reviews = data.reviews;  // Make sure the backend sends an array of reviews
      },
      methods: {
        startReviewEdit(r: Review) {
          this.editingId = r.id
          this.editedReview = {
            name: r.name,
            restaurantId: r.restaurant.id,
            rating: r.rating,
            food_rating: r.food_rating,
            service_rating: r.service_rating,
            ambience_rating: r.ambience_rating,
            description: r.description
          }
        },

        cancelReviewEdit() {
          this.editingId = null
        },

        async saveReviewEdit(id: number) {
          try {
            const payload = {
              name: this.editedReview.name.trim(),
              restaurant_id: this.editedReview.restaurantId,
              rating: this.editedReview.rating,
              food_rating: this.editedReview.food_rating,
              service_rating: this.editedReview.service_rating,
              ambience_rating: this.editedReview.ambience_rating,
              description: this.editedReview.description.trim(),
            }

            const res = await fetch(`http://localhost:8000/review/${id}/`, {
              method: 'PUT',
              headers: {
                'Authorization': `Bearer ${VueCookies.get('access_token')}`,
                'Content-Type': 'application/json',
                'X-CSRFToken': VueCookies.get('csrftoken'),
              },
              credentials: 'include',
              body: JSON.stringify(payload)
            })
            if (!res.ok) throw new Error('Update failed')

            const updated = await res.json()

            // update your local array
            const idx = this.reviews.findIndex(r => r.id === id)
            if (idx > -1) this.reviews.splice(idx, 1, updated.review)

            this.cancelReviewEdit()
            window.location.reload();
            alert('Review updated!')
          } catch (e) {
            console.error(e)
            alert('Could not save changes.')
          }
        },
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
                restaurant_id: this.newReview.restaurant.id,
                rating: this.newReview.rating,
                food_rating: this.newReview.food_rating,
                service_rating:this.newReview.service_rating,
                ambience_rating:this.newReview.ambience_rating,
                description: this.newReview.description,  
                date: this.newReview.date,
                user_id: userId,
            };

            try {
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
                window.location.reload();
                alert('Review added successfully!');
            } catch (error) {
              console.error('Error creating reservation:', error);
              alert('Failed to create reservation');
            }
        },
        async deleteReview(reviewId: number) {
            // Check if the logged-in user is the one who wrote the review
            const reviewToDelete = this.reviews.find(review => review.id === reviewId);
            if (!reviewToDelete || !reviewToDelete.user || reviewToDelete.user.id !== this.user.id) {
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
        restaurants(): Restaurant[]{
            const restaurantsStore = useRestaurantsStore;
            return this.restaurantsStore.restaurants; // Bind to the fetched cuisine data from Pinia store
        },
        filteredReviews() {
          if (!this.searchRestaurant) return this.reviews;
          return this.reviews.filter(review =>
            review.restaurant?.name?.toLowerCase().includes(this.searchRestaurant.toLowerCase())
          );
        },
        paginatedReviews() {
            const start = (this.currentPage - 1) * this.itemsPerPage;
            const end = start + this.itemsPerPage;
            return this.filteredReviews.slice(start, end);
        },
        totalPages() {
            return Math.ceil(this.filteredReviews.length / this.itemsPerPage);
        },
    
      },
      setup() {
          const userStore = useUserStore();
          const reviewsStore = useReviewsStore();
          const restaurantsStore = useRestaurantsStore();
          const usersStore = useUsersStore();
          return { userStore , reviewsStore , usersStore, restaurantsStore};
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

  .review-page {
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

  .review-header h3 {
    margin: 0;
    color: var(--accent);
  }

  .review-header p {
    margin: 0.25rem 0 1rem;
    font-size: 0.9rem;
    color: var(--muted);
  }

  .review-content {
    color: var(--text);
    line-height: 1.5;
    margin-bottom: 1rem;
  }

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

  @media (max-width: 800px) {
    .review-page {
      padding: 1rem;
    }
  }
</style>
