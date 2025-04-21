<template>
  <div class="body">
     <div id="profile-box">
        <h2>Welcome {{ user.first_name }}</h2>
    </div>
    <div class="restaurant">
        <label for="restaurants">Choose a restaurant to add to your wishlist:</label>
        <select id="restaurants" v-model="chosenRestaurant">
            <option v-for="restaurant in restaurants">
                {{ restaurant.name }}
            </option>
        </select>
        <button @click="addChosen">Save Choice Here</button>
        <div class="restaurants">
                <h4>restaurants</h4>
                  <ul v-for="(chosen, index) in chosens" :key="index">
                  <li class="friends" v-if="chosen.user==user.id">
                      {{ chosen.name }} <button @click="deleteChosen(chosen.id)"> Delete </button>
                  </li>
              </ul>
          </div>
    </div>
  </div>
  
  
</template>

<script lang="ts">
  import { defineComponent } from "vue";
  import { User, Restaurant, Friendship, Chosen,Cuisine, ChosenCuisine, Allergy, ChosenAllergy} from "../types/index";
  import { useUserStore } from "../stores/user";
  import { useUsersStore } from "../stores/users";
  import { useRestaurantsStore } from "../stores/restaurants";
  import { useAllergysStore } from "../stores/allergys";
  import { useChosenAllergyStore } from "../stores/chosenAllergy";
  import { useCuisinesStore } from "../stores/cuisines"; 
  import { useChosenAllergysStore } from "../stores/chosenAllergys";
  import { useChosenStore } from "../stores/chosen";
  import { useChosensStore } from "../stores/chosens";
  import { useChosenCuisineStore } from "../stores/chosenCuisine";
  import { useChosenCuisinesStore } from "../stores/chosenCuisines";
  import { useFriendshipsStore } from "../stores/friendships";
  import VueCookies from 'vue-cookies';

  


  export default defineComponent({
      data() {
          return {
          editFirstName: false,
          editLastName: false,
          editEmail: false,
          editDateOfBirth: false,
          
          editedUser: {
              first_name: "",
              last_name: "",
              email: "",
              date_of_birth: "",
              
          },
          
          chosenRestaurant: "",
          chosenChosenAllergys: "",
          chosenChosenCuisines: "",
          recommendedRestaurants: [],
          chosenAllergy: [],
          chosenCuisine:[],
          
          
          };
      },
      async mounted() {
          console.log(this.user.userType); 
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
                  console.log(this.user.user_type); 
                  
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

          // Fetching all cuisines from the backend
          let res = await fetch(`http://localhost:8000/cuisines/`);
          let cuisineData = await res.json();

          // Update the state with the fetched cuisine data
          let madeCuisines = cuisineData.cuisines as Cuisine[];
          const cuisinesStore = useCuisinesStore();
          cuisinesStore.saveCuisines(madeCuisines); 
          console.log(res)

          //fetch all the friendships
          let responseFriendship = await fetch("http://localhost:8000/friendships/");
          let dataFriendship = await responseFriendship.json();
          let friendships = dataFriendship.friendships as Friendship[];

          const storeFriendships = useFriendshipsStore();
          storeFriendships.saveFriendships(friendships);

          //fetch all the friendships
          let responseChosen = await fetch("http://localhost:8000/chosens/");
          let dataChosen = await responseChosen.json();
          let chosens = dataChosen.chosens as Chosen[];
  
          const storeChosens = useChosensStore();
          storeChosens.saveChosens(chosens);

          //fetch all the friendships
          let responseChosenCuisine = await fetch("http://localhost:8000/chosenCuisines/");
          let dataChosenCuisine = await responseChosenCuisine.json();
          let chosenCuisines = dataChosenCuisine.chosenCuisines as ChosenCuisine[];

          const storeChosenCuisines = useChosenCuisinesStore();
          storeChosenCuisines.saveChosenCuisines(chosenCuisines);


          // Fetching all cuisines from the backend
          let resA = await fetch(`http://localhost:8000/allergys/`);
          let allergyData = await resA.json();

          // Update the state with the fetched allergy data
          let madeAllergys = allergyData.allergys as Allergy[];
          const allergysStore = useAllergysStore();
          allergysStore.saveAllergys(madeAllergys); 
          console.log(resA)

          //fetch all the friendships
          let responseChosenAllergy = await fetch("http://localhost:8000/chosenAllergys/");
          let dataChosenAllergy = await responseChosenAllergy.json();
          let chosenAllergys = dataChosenAllergy.chosenAllergys as ChosenAllergy[];

          const storeChosenAllergys = useChosenAllergysStore();
          storeChosenAllergys.saveChosenAllergys(chosenAllergys);

          await this.getUserPreferences();


          
      },
      methods: {
          //console.log(user.userType)
          toggleEditField(field: string) {
            console.log(typeof field)
              this[`edit${field}`] = !this[`edit${field}`];
              if (this[`edit${field}`]) {
                  this.editedUser[field.toLowerCase()] = this.user[field.toLowerCase()];
              }
              //this.editPassword = !this.editPassword; // Toggle edit mode
          },

          // Fetch the current user's chosen cuisines and allergies
           // Fetch the current user's chosen cuisines and allergies
          async getUserPreferences() {
            const user = this.userStore.user;
            console.log('Updated Chosen Cuisines:', this.chosenCuisines);


            // Ensure that chosenCuisine and allergies are defined, default to empty array if not
            this.chosenCuisines = user.chosenCuisines || [];  // Default to empty array if undefined
            this.chosenAllergys = user.chosenAllergys || [];  // Default to empty array if undefined

            console.log("Chosen Cuisines:", this.chosenCuisines);
            console.log("Allergies:", this.chosenAllergys);

            // Now fetch the recommended restaurants based on preferences
            await this.getRecommendedRestaurants();
          },
          // Fetch the recommended restaurants from the backend
          async getRecommendedRestaurants() {
            // Get the IDs for the chosen cuisines and allergies
            const cuisineIds = this.chosenCuisines
              .filter(c => c.user === this.user.id)
              .map(c => c.cuisine)

            const allergyIds = this.chosenAllergys
              .filter(a => a.user === this.user.id)
              .map(a => a.allergy)
            try {
              const response = await fetch("http://localhost:8000/recommend_restaurants/", {
                method: "POST",
                headers: {
                  'Authorization': `Bearer ${VueCookies.get('access_token')}`,
                  'Content-Type': 'application/json',
                  'X-CSRFToken': VueCookies.get('csrftoken'),
                },
                credentials: 'include',
                body: JSON.stringify({
                  cuisines: cuisineIds,  // Send cuisines' IDs in the request body
                  allergys: allergyIds,  // Send allergies' IDs in the request body
                }),
              });

              if (response.ok) {
                const data = await response.json();
                this.recommendedRestaurants = data.restaurants;  // Set the fetched recommended restaurants
                console.log("Recommended Restaurants:", this.recommendedRestaurants);
              } else {
                console.error('Failed to fetch recommended restaurants');
              }
            } catch (error) {
              console.error('Error fetching recommended restaurants:', error);
            }
          },
        

        
          
          async saveField(field: string) {
             
              try {
                  
                  const payload = {
                      [field.toLowerCase()]: this.editedUser[field.toLowerCase()],
                  };
                  console.log(payload)
                  const response = await fetch(`http://localhost:8000/user/${this.user.id}/`, {
                      method: "PUT",
                      headers: {
                          'Authorization': `Bearer ${VueCookies.get('access_token')}`,
                          'Content-Type': 'application/json',
                          'X-CSRFToken': VueCookies.get('csrftoken'),
                      },
                      credentials: 'include',
                      body: JSON.stringify(payload),
                  });
              
                  console.log("CSRF Token:", this.userStore.csrf);

                  if (!response.ok) {
                      throw new Error("Failed to update field");
                  }

                  const updatedUser = await response.json();
                  console.log(updatedUser)
                  this.userStore = this.userStore.saveUsers(updatedUser); // Update the user state in the store
                  window.location.reload();
                  alert(`${field} updated successfully!`);
              } catch (error) {
                  console.error(error);
                  alert(`Failed to update ${field}.`);
              }
          },
        


          
          //deletes the friendships between users and friend whether pending or accepted
          async deleteChosen(chosenId: number) {
       
            try {
              const response = await fetch(`http://localhost:8000/chosen/${chosenId}/`, {
                method: "DELETE",
                headers: {
                  "Authorization": `Bearer ${VueCookies.get("access_token")}`,
                  "Content-Type": "application/json",
                  "X-CSRFToken": VueCookies.get("csrftoken"),
                },
                credentials: "include",
              });

              if (!response.ok) {
                throw new Error("Failed to delete chosen restaurant");
              }

              //Remove the deleted friendship from the store
              const chosensStore = useChosensStore();
              chosensStore.removeChosen(chosenId);

              window.location.reload();
              alert("Chosen restaurant deleted successfully!");
            } catch (error) {
              console.error("Error deleting chosen restaurant:", error);
              alert("Failed to delete chosen restaurant. Please try again.");
            }
          },

          async addChosen() {
            if (this.chosenRestaurant === "") {
                alert("Invalid restaurant Choice.");
                return;
            }

            const chosensStore = useChosensStore();
            const restaurantsStore = useRestaurantsStore();
            const chosenRestaurantLower = this.chosenRestaurant.toLowerCase();

            // Check if the logged-in user has already chosen this restaurant
            let alreadyChosenByUser = chosensStore.chosens.some(chosen => chosen.user === this.user.id && chosen.name.toLowerCase() === chosenRestaurantLower);
            
            if (alreadyChosenByUser) {
                alert("You have already chosen this restaurant.");
                return;
            }

            // Find the restaurant from the restaurant store
            let foundRestaurant = restaurantsStore.getRestaurantByName(this.chosenRestaurant);
            if (!foundRestaurant) {
                alert("restaurant not found.");
                return;
            }

            const foundRestaurantId = foundRestaurant.id;

            // Prepare the payload for creating a new chosen restaurant
            const payload = {
                user_id: this.user.id,
                restaurant_id: foundRestaurantId,
            };

            // Send POST request to create a chosen restaurant
            const chosenResponse = await fetch("http://localhost:8000/chosens/", {
                method: "POST",
                headers: {
                Authorization: `Bearer ${VueCookies.get("access_token")}`,
                "Content-Type": "application/json",
                "X-CSRFToken": VueCookies.get("csrftoken"),
                },
                credentials: "include",
                body: JSON.stringify(payload),
            });

            // If the response is successful, add the new chosen restaurant to the store
            if (chosenResponse.ok) {
                const data = await chosenResponse.json();
                const createdChosen = data.chosen as Chosen;
                chosensStore.addChosen(createdChosen);

                window.location.reload(); // Refresh the page to reflect the changes
                alert("Restaurant added to wishlist successfully!");
            } else {
                alert("Failed to add the restaurant. Please try again.");
            }
            },
           // Accepts the pending friendship between user and friend it then makes an accepted friendship between friend and user
           //This means the friendship is symmetrical 
           async acceptFriendship(friendshipId: number) {
              try {
                  const acceptResponse = await fetch(`http://localhost:8000/friendship/${friendshipId}/`, {
                      method: "PUT",
                      headers: {
                          "Authorization": `Bearer ${VueCookies.get("access_token")}`,
                          "Content-Type": "application/json",
                          "X-CSRFToken": VueCookies.get("csrftoken"),
                      },
                      credentials: "include",
                  });

                  if (!acceptResponse.ok) {
                      throw new Error("Failed to accept friendship.");
                  }

                  const dataAccept = await acceptResponse.json();
                  const newAccept = dataAccept.friendship as Friendship;

                  // Update the friendship in the store
                  const friendshipsStore = useFriendshipsStore();
                  friendshipsStore.addFriendship(newAccept);
                  window.location.reload();
                  alert(`Accepted successfully!`);
              } catch (error) {
                  console.error("Error accepting friendship:", error);
                  alert("Failed to accept friendship. Please try again.");
              }
          },
          //rejects the friendships between users and friend whether pending or accepted
          async deleteFriendship(friendshipId: number) {
            console.log(friendshipId)
            try {
              const response = await fetch(`http://localhost:8000/friendship/${friendshipId}/`, {
                method: "DELETE",
                headers: {
                  "Authorization": `Bearer ${VueCookies.get("access_token")}`,
                  "Content-Type": "application/json",
                  "X-CSRFToken": VueCookies.get("csrftoken"),
                },
                credentials: "include",
              });

              if (!response.ok) {
                throw new Error("Failed to delete friendship");
              }

              //Remove the deleted friendship from the store
              const friendshipsStore = useFriendshipsStore();
              friendshipsStore.removeFriendship(friendshipId);

              window.location.reload();
              alert("Friendship deleted successfully!");
            } catch (error) {
              console.error("Error deleting friendship:", error);
              alert("Failed to delete friendship. Please try again.");
            }
          },
          //deletes the friendships between users and friend whether pending or accepted
          async deleteChosenCuisine(chosenCuisineId: number) {
       
            try {
              const response = await fetch(`http://localhost:8000/chosenCuisine/${chosenCuisineId}/`, {
                method: "DELETE",
                headers: {
                  "Authorization": `Bearer ${VueCookies.get("access_token")}`,
                  "Content-Type": "application/json",
                  "X-CSRFToken": VueCookies.get("csrftoken"),
                },
                credentials: "include",
              });

              if (!response.ok) {
                throw new Error("Failed to delete chosen cuisine");
              }

              //Remove the deleted friendship from the store
              const chosenCuisinesStore = useChosenCuisinesStore();
              //chosenCuisinesStore.removeChosenCuisine(chosenCuisineId);

              window.location.reload();
              alert("Chosen cuisine deleted successfully!");
            } catch (error) {
              console.error("Error deleting chosen cuisine:", error);
              alert("Failed to delete chosen cuisine. Please try again.");
            }
          },

          async addChosenCuisine() {
            if (this.chosenChosenCuisine === "") {
                alert("Invalid cuisine Choice.");
                return;
            }

            const chosenCuisinesStore = useChosenCuisinesStore();
            const cuisinesStore = useCuisinesStore();
            const chosenChosenCuisineLower = this.chosenChosenCuisine.toLowerCase();

            // Check if the logged-in user has already chosen this cusine
            let alreadyChosenCuisineByUser = chosenCuisinesStore.chosenCuisines.some(chosenCuisine => chosenCuisine.user === this.user.id && chosenCuisine.name.toLowerCase() === chosenChosenCuisineLower);
            
            if (alreadyChosenCuisineByUser) {
                alert("You have already chosen this cuisine.");
                return;
            }

            // Find the cuisine from the cuisine store
            let foundCuisine = cuisinesStore.getCuisineByName(this.chosenChosenCuisine);
            if (!foundCuisine) {
                alert("cuisine not found.");
                return;
            }

            const foundCuisineId = foundCuisine.id;

            // Prepare the payload for creating a new chosen cuisine
            const payload = {
                user_id: this.user.id,
                cuisine_id: foundCuisineId,
            };

            // Send POST request to create a chosen cuisine
            const chosenCuisineResponse = await fetch("http://localhost:8000/chosenCuisines/", {
                method: "POST",
                headers: {
                Authorization: `Bearer ${VueCookies.get("access_token")}`,
                "Content-Type": "application/json",
                "X-CSRFToken": VueCookies.get("csrftoken"),
                },
                credentials: "include",
                body: JSON.stringify(payload),
            });

            // If the response is successful, add the new chosen restaurant to the store
            if (chosenCuisineResponse.ok) {
                const dataC = await chosenCuisineResponse.json();
                const createdChosenCuisine = dataC.chosenCuisine as ChosenCuisine;
                //chosenCuisinesStore.addChosenCuisine(createdChosenCuisine);

                window.location.reload(); // Refresh the page to reflect the changes
                alert("Chosen cuisine added successfully!");
            } else {
                alert("Failed to add the chosen cuisine. Please try again.");
            }
          },


           //deletes the friendships between users and friend whether pending or accepted
          async deleteChosenAllergy(chosenAllergyId: number) {
       
            try {
              const response = await fetch(`http://localhost:8000/chosenAllergy/${chosenAllergyId}/`, {
                method: "DELETE",
                headers: {
                  "Authorization": `Bearer ${VueCookies.get("access_token")}`,
                  "Content-Type": "application/json",
                  "X-CSRFToken": VueCookies.get("csrftoken"),
                },
                credentials: "include",
              });

              if (!response.ok) {
                throw new Error("Failed to delete chosen allergy");
              }

              //Remove the deleted friendship from the store
              const chosenAllergysStore = useChosenAllergysStore();
              //chosenCuisinesStore.removeChosenCuisine(chosenCuisineId);

              window.location.reload();
              alert("Chosen allergy deleted successfully!");
            } catch (error) {
              console.error("Error deleting chosen allergy:", error);
              alert("Failed to delete chosen allergy. Please try again.");
            }
          },

          async addChosenAllergy() {
            if (this.chosenChosenAllergy === "") {
                alert("Invalid allergy Choice.");
                return;
            }

            const chosenAllergysStore = useChosenAllergysStore();
            const allergysStore = useAllergysStore();
            const chosenChosenAllergyLower = this.chosenChosenAllergy.toLowerCase();

            // Check if the logged-in user has already chosen this cusine
            let alreadyChosenAllergyByUser = chosenAllergysStore.chosenAllergys.some(chosenAllergy => chosenAllergy.user === this.user.id && chosenAllergy.name.toLowerCase() === chosenChosenAllergyLower);
            
            if (alreadyChosenAllergyByUser) {
                alert("You have already chosen this allergy.");
                return;
            }

            // Find the cuisine from the cuisine store
            let foundAllergy = allergysStore.getAllergyByName(this.chosenChosenAllergy);
            if (!foundAllergy) {
                alert("Allergy not found.");
                return;
            }

            const foundAllergyId = foundAllergy.id;

            // Prepare the payload for creating a new chosen Allergy
            const payload = {
                user_id: this.user.id,
                allergy_id: foundAllergyId,
            };

            // Send POST request to create a chosen Allergy
            const chosenAllergyResponse = await fetch("http://localhost:8000/chosenAllergys/", {
                method: "POST",
                headers: {
                Authorization: `Bearer ${VueCookies.get("access_token")}`,
                "Content-Type": "application/json",
                "X-CSRFToken": VueCookies.get("csrftoken"),
                },
                credentials: "include",
                body: JSON.stringify(payload),
            });

            // If the response is successful, add the new chosen restaurant to the store
            if (chosenAllergyResponse.ok) {
                const dataC = await chosenAllergyResponse.json();
                const createdChosenAllergy = dataC.chosenAllergy as ChosenAllergy;
                //chosenCuisinesStore.addChosenCuisine(createdChosenCuisine);

                window.location.reload(); // Refresh the page to reflect the changes
                alert("Chosen Allergy added successfully!");
            } else {
                alert("Failed to add the chosen Allergy. Please try again.");
            }
          },


      }, 
      computed: {
          user() {
              const userStore = useUserStore;
              return this.userStore.user; // Bind to the fetched user data from Pinia store
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
          friendships(){
              const friendshipsStore = useFriendshipsStore;
              return this.friendshipsStore.friendships;
          },
          chosens(){
              const chosensStore = useChosensStore;
              return this.chosensStore.chosens;
          },
          chosenCuisines(){
              const chosenCuisinesStore = useChosenCuisinesStore;
              return this.chosenCuisinesStore.chosenCuisines;
          },
          chosenAllergys(){
              const chosenAllergysStore = useChosenAllergysStore;
              return this.chosenAllergysStore.chosenAllergys;
          },
    
      },
      setup() {
          const userStore = useUserStore();
          const restaurantsStore = useRestaurantsStore();
          const allergysStore = useAllergysStore();
          const chosenAllergysStore = useChosenAllergysStore();
          const friendshipsStore = useFriendshipsStore();
          const usersStore = useUsersStore();
          const chosensStore = useChosensStore();
          const chosenCuisinesStore = useChosenCuisinesStore();
          const cuisinesStore = useCuisinesStore();
          return { userStore , restaurantsStore , friendshipsStore, usersStore, chosensStore, chosenCuisinesStore, cuisinesStore, chosenAllergysStore, allergysStore};
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

/* 2) Page background & font */
.body {
  font-family: 'Segoe UI', sans-serif;
  color: var(--text);
  background: linear-gradient(135deg, var(--bg-start), var(--bg-end));
  min-height: 100vh;
  padding: 2rem;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

/* 3) Profile box card */
#profile-box {
  background: var(--card-bg);
  border-radius: var(--radius);
  box-shadow: 0 4px 20px rgba(0,0,0,0.4);
  padding: 1.5rem;
}

/* 4) Restaurant selector card */
.restaurant {
  background: var(--card-bg);
  border-radius: var(--radius);
  box-shadow: 0 4px 20px rgba(0,0,0,0.4);
  padding: 1.5rem;
}

/* 5) Headings */
#profile-box h2,
.restaurant h4 {
  margin-top: 0;
  color: var(--text);
  border-bottom: 1px solid rgba(255,255,255,0.2);
  padding-bottom: 0.5rem;
}

/* 6) Select inputs */
select {
  width: 100%;
  padding: 0.6rem 0.8rem;
  background: rgba(255,255,255,0.1);
  border: none;
  border-radius: var(--radius);
  color: var(--text);
  margin-bottom: 1rem;
}

/* 7) Neon‑gradient buttons */
a,
button {
  background: linear-gradient(90deg, #ff0080, #ff8c00);
  border: none;
  padding: 0.6rem 1.2rem;
  color: white;
  font-weight: 600;
  border-radius: var(--radius);
  cursor: pointer;
  text-decoration: none;
  display: inline-block;
  transition: transform .15s ease;
}

a:hover,
button:hover {
  transform: scale(1.05);
}

/* 8) List of chosen restaurants */
.restaurants {
  margin-top: 1.5rem;
}

.restaurants ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.restaurants li {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: rgba(255,255,255,0.1);
  padding: 0.6rem 1rem;
  border-radius: var(--radius);
  margin-bottom: 0.75rem;
  color: var(--text);
}

/* 9) Delete buttons */
.restaurants li button {
  background: #ff4e4e;
  padding: 0.4rem 0.8rem;
  font-size: 0.85rem;
}

.restaurants li button:hover {
  background: #ff1c1c;
}

/* 10) Responsive */
@media (max-width: 800px) {
  .body {
    grid-template-columns: 1fr;
  }
}
</style>

