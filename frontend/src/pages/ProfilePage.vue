<template>
  <div class="body">
  <div v-if="this.user.user_type == 'Owner'"> 
    <RouterLink  to="/restaurants">Add or view Restaurants</RouterLink>
    <RouterLink  to="/confirms">View Reservations</RouterLink>
  

  </div>
     <div id="profile-box">
     
        <h2>Welcome {{ user.first_name }}</h2>
            <p>
            Username: {{ user.username }}
            
            
            <button> <a href="http://localhost:8000/updateUser/"> Change Username </a> </button>
            
            </p>
        
          <p>
              <span v-if="!editFirstName">First Name: {{ user.first_name }}</span>
                  <span v-else>
                      First Name:
                      <input v-model="editedUser.first_name" type="text" />
                  </span>
                  <button v-if="!editFirstName" @click="toggleEditField('FirstName')">Edit</button>
                  <button v-else @click="saveField('first_name')">Save</button>
          </p>
          
          <p>
              <span v-if="!editLastName">Last Name: {{ user.last_name }}</span>
                  <span v-else>
                      Last Name:
                      <input v-model="editedUser.last_name" type="text" />
                  </span>
                  <button v-if="!editLastName" @click="toggleEditField('LastName')">Edit</button>
                  <button v-else @click="saveField('last_name')">Save</button>
          </p>
          <p>
              <span v-if="!editEmail">Email: {{ user.email }}</span>
              <span v-else>
                  Email:
                  <input v-model="editedUser.email" type="email" />
              </span>
              <button v-if="!editEmail" @click="toggleEditField('Email')">Edit</button>
              <button v-else @click="saveField('email')">Save</button>
          </p>
          <p>
          <span v-if="!editDateOfBirth">Date of Birth: {{ user.date_of_birth }}</span>
              <span v-else>
                  {{ user.date_of_birth }}
                  <input v-model="editedUser.date_of_birth" type="date" />
              </span>
              <button v-if="!editDateOfBirth" @click="toggleEditField('DateOfBirth')">Edit</button>
              <button v-else @click="saveField('date_of_birth')">Save</button>
          </p>
          <p>
                <span v-if="!editPassword">Password: ********</span>
            
                <button> <a href="http://localhost:8000/updatePass/"> Change Password </a> </button>
                
          </p>
          <p>
              <span >User type: {{ user.user_type }}</span>
          </p>
         
    </div>
    
    <div class="restaurant">
        <label for="restaurants">Choose a restaurant:</label>
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

    <div class="cuisine">
        <label for="cuisines">Choose a cuisine:</label>
        <select id="cuisines" v-model="this.chosenChosenCuisine">
            <option v-for="cuisine in cuisines">
                {{ cuisine.name }}
            </option>
        </select>
        <button @click="addChosenCuisine">Save Choice Here</button>
        <div class="cuisines">
                <h4>cuisines</h4>
                  <ul v-for="(chosenCuisine, index) in chosenCuisines" :key="index">
                  <li class="friends" v-if="chosenCuisine.user==user.id">
                      {{ chosenCuisine.name }} <button @click="deleteChosenCuisine(chosenCuisine.id)"> Delete </button>
                  </li>
              </ul>
              
          </div>
    </div>
        
      
      <div class="friend-accepted">
          <div>
              <h2>Accepted Friends</h2>
          </div>

          <ul v-for="(friendship, index) in friendships" :key="index">
              <li class="friends" v-if="friendship.user==user.id && friendship.accepted == true">
                  {{ friendship.username }} <button @click="deleteFriendship(friendship.id)"> Delete </button>
              </li>
          </ul>
        
     </div>

     <div  class="friend-pending">
          <div>
              <h2>Pending Friends</h2>
          </div>

          <ul v-for="(friendship, index) in friendships" :key="index">
              <li class="friends" v-if="friendship.user==user.id && friendship.accepted == false">
                  {{ friendship.username }} 
                  <button @click="deleteFriendship(friendship.id)"> Delete </button>
                  <button @click="acceptFriendship(friendship.id)"> Accept </button>
              </li>
          </ul>
        
     </div>

    
  </div>
  
  
</template>

<script lang="ts">
  import { defineComponent } from "vue";
  import { User, Restaurant, Friendship, Chosen,Cuisine, ChosenCuisine} from "../types/index";
  import { useUserStore } from "../stores/user";
  import { useUsersStore } from "../stores/users";
  import { useRestaurantsStore } from "../stores/restaurants";

  import { useCuisinesStore } from "../stores/cuisines";
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
          
          chosenChosenCuisine: "",
          
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
                alert("Chosen restaurant added successfully!");
            } else {
                alert("Failed to add the chosen restaurant. Please try again.");
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
    
      },
      setup() {
          const userStore = useUserStore();
          const restaurantsStore = useRestaurantsStore();
          const cuisinesStore = useCuisinesStore();
          const friendshipsStore = useFriendshipsStore();
          const usersStore = useUsersStore();
          const chosensStore = useChosensStore();
          const chosenCuisinesStore = useChosenCuisinesStore();
          return { userStore , restaurantsStore , friendshipsStore, usersStore, chosensStore, chosenCuisinesStore, cuisinesStore};
      },
  });
  </script>


<style scoped>
  /* General layout and body styling */
  .body {
    font-family: Arial, Helvetica, sans-serif;
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: auto auto auto auto auto;
    gap: 1rem 0.25rem;
    background-color: #B4DABA; /* Light background */
    padding: 2em;
  }

  /* Profile box */
  #profile-box {
    grid-column: 1;
    grid-row: 1 / span 2;
    background-color: #659A78; /* Olive green background */
    padding: 2em;
    border-radius: 1rem;
  }

  /* Restaurant section */
  #restaurant {
    grid-column: 1;
    grid-row: 3;
    padding: 2rem;
    background-color: #D9D9D9; /* Light gray */
    border-radius: 1rem;
  }

  /* Create restaurant section */
  #create-restaurant {
    grid-column: 1;
    grid-row: 4;
    background-color: rgb(243, 163, 163); /* Light pinkish background */
    padding: 2rem;
    border-radius: 1rem;
  }

  #create-restaurant h3 {
    text-align: center;
    font-size: 1.5rem;
    margin-bottom: 1rem;
    color: #333;
  }

  #create-restaurant input,
  #create-restaurant textarea {
    width: 100%;
    margin-bottom: 1.5rem;
    padding: 1rem;
    border: 1px solid #B4DABA;
    border-radius: 1rem;
    background-color: #fff;
  }

  /* Friend sections (accepted and pending) */
  .friend-accepted,
  .friend-pending {
    background-color: rgb(243, 163, 163); /* Light pinkish background */
    padding: 2em;
    border-radius: 1rem;
  }

  .friend-accepted {
    grid-column: 2;
    grid-row: 1 / span 2;
  }

  .friend-pending {
    grid-column: 2;
    grid-row: 3 / span 2;
  }

  /* Button and link styles */
  a,
  button {
    background-color: rgb(243, 163, 163); /* Light pinkish background */
    color: white;
    padding: 0.7rem 2rem;
    font-size: 1rem;
    border: none;
    border-radius: 1rem;
    cursor: pointer;
    display: block;
    margin: 0 auto;
    text-decoration: none;
  }

  a:hover,
  button:hover {
    background-color: #D9D9D9; /* Light gray */
    color: #333;
  }

  /* Restaurant list */
  .restaurants {
    background-color: rgb(243, 163, 163); /* Light pinkish background */
    padding: 2rem;
    border-radius: 1rem;
  }

  .restaurants h2 {
    text-align: center;
    font-size: 2rem;
    color: #333;
  }

  .restaurant-item {
    background-color: #f9f9f9;
    padding: 1rem;
    margin-bottom: 1rem;
    border-radius: 1rem;
    box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.1);
  }

  .restaurant-header h3 {
    font-size: 1.5rem;
    font-weight: bold;
    color: #333;
  }

  .restaurant-header p {
    margin: 0.5rem 0;
    color: #777;
  }

  /* Review section */
  .review-item {
    background-color: #f9f9f9;
    margin-bottom: 1.5rem;
    padding: 1rem;
    border-radius: 1rem;
    box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.1);
  }

  .review-header h3 {
    font-size: 1.5rem;
    font-weight: bold;
    color: #333;
  }

  .review-header p {
    margin: 0.5rem 0;
    color: #777;
    font-size: 1rem;
  }

  .review-content {
    font-size: 1.2rem;
    line-height: 1.6;
    color: #333;
  }

  /* Review actions (delete, etc.) */
  .review-actions button {
    background-color: #ff4e4e;
    color: white;
    padding: 0.5rem 1rem;
    font-size: 1rem;
    cursor: pointer;
    border-radius: 1rem;
    border: none;
  }

  .review-actions button:hover {
    background-color: #ff1c1c;
  }

  /* Additional link styling */
  a {
    text-decoration: none;
    color: black;
    background-color: #659A78;
    padding: 0.5em;
    border-radius: 1rem;
  }

  a:hover {
    color: white;
    background-color: #D9D9D9;
  }
</style>

