<template>
  <div>
    <h2>Potential Friends</h2>

    <!-- Age filter controls -->
    <div style="margin-bottom: 1rem;">
      <label for="minAge">Min Age:</label>
      <input id="minAge" type="number" v-model="filterAgeMin" />

      <label for="maxAge">Max Age:</label>
      <input id="maxAge" type="number" v-model="filterAgeMax" />
    </div>

    <table>
      <thead>
        <tr>
          <th>Username</th>
          <th>Age</th>
          <th>Hobbies</th>
          <th>Request Friends</th>
        </tr>
      </thead>
      <tbody>
        <!-- Render paginatedData which will already be filtered by age -->
        <tr v-for="(user, index) in paginatedData" :key="index">
        
            <td v-if="!isFriend(user.id)">{{ user.username }}</td>
            <td v-if="!isFriend(user.id)">{{ getAge(user.date_of_birth) }}</td>
            <td v-if="!isFriend(user.id)">
              <ul v-for="(chosen, index) in chosens" :key="index">
                <li v-if="chosen.user==user.id">
                    {{ chosen.name }} 
                </li>
              </ul>
            </td>
         
          <td v-if="!isFriend(user.id)"><button @click="addFriendship(user.id)">Request</button></td>


        </tr>
      </tbody>
    </table>

    <!-- Pagination Controls -->
    <div class="pagination">
      <button @click="prevPage" :disabled="currentPage === 1">Previous</button>
      <span>Page {{ currentPage }} of {{ totalPages }}</span>
      <button @click="nextPage" :disabled="currentPage === totalPages">Next</button>
    </div>

  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { useUsersStore } from "../stores/users";

import { User, Friendship, Chosen } from "../types";
import { useFriendshipsStore } from "../stores/friendships";
import { useUserStore } from "../stores/user";

import VueCookies from 'vue-cookies';
import { useChosensStore } from "../stores/chosens";

export default defineComponent({
  data() {
    return {
      // Pagination
      currentPage: 1,
      rowsPerPage: 10,

      //Age filters
      filterAgeMin: 0,
      filterAgeMax: 100, 
      
      //fetch user id
      user_id : Number(window.sessionStorage.getItem("user_id")),

      
      
    };
  },

  async mounted() {
    let response = await fetch("http://localhost:8000/users/");
    let data = await response.json();
    let users = data.users as User[];
    const store = useUsersStore()
    store.saveUsers(users)

    let responseFriendship = await fetch("http://localhost:8000/friendships/");
    let dataFriendship = await responseFriendship.json();
    let friendships = dataFriendship.friendships as Friendship[];

    const storeFriendships = useFriendshipsStore();
    storeFriendships.saveFriendships(friendships as Friendship[]);

    let responseChosen = await fetch("http://localhost:8000/chosens/");
    let dataChosen = await responseChosen.json();
    let chosens = dataChosen.chosens as Chosen[];

    const storeChosens = useChosensStore();
    storeChosens.saveChosens(chosens as Chosen[]);


  },

  computed: {
    chosens(){
              const chosensStore = useChosensStore;
              return this.chosensStore.chosens;
      },
      // Filter the users array first based on the selected age range and sort by similarity
      filteredUsers(): User[] {
        const store = useUsersStore();
        const loggedInUserHobbies = this.chosens.filter(chosen => chosen.user === this.user_id).map(chosen => chosen.name.toLowerCase());

        // Filter users based on the age range
        const filtered = store.users.filter(user => {
          const age = this.getAge(user.date_of_birth);
          return age >= this.filterAgeMin && age <= this.filterAgeMax;
        });

        // Sort users by the number of common hobbies with the logged-in user
        return filtered
          .map(user => {
            // Get the hobbies of the user being evaluated
            const userHobbies = this.chosens.filter(chosen => chosen.user === user.id).map(chosen => chosen.name.toLowerCase());

            // Calculate similarity score
            const similarityScore = this.calculateSimilarity(loggedInUserHobbies, userHobbies);

            // Ensure similarity score is set to 0 if no hobbies
            return { ...user, userHobbies, similarityScore: similarityScore || 0, hasHobbies: userHobbies.length > 0 };
          })
          .sort((a, b) => {
            // First, sort by whether the user has hobbies or not (no hobbies goes to the bottom)
            if (a.hasHobbies !== b.hasHobbies) {
              return a.hasHobbies ? -1 : 1;
            }

            // Then, sort by similarity score (higher similarity goes first)
            return b.similarityScore - a.similarityScore;
          });
      },


    //  Total pages based on filtered users
    totalPages(): number {
      return Math.ceil(this.filteredUsers.length / this.rowsPerPage);
    },

    // Slice the filtered array for pagination
    paginatedData(): User[] {
      const startIndex = (this.currentPage - 1) * this.rowsPerPage;
      const endIndex = startIndex + this.rowsPerPage;
      return this.filteredUsers.slice(startIndex, endIndex);
    },
  },

  methods: {
    // Calculate similarity score based on shared hobbies
    calculateSimilarity(loggedInHobbies: string[], userHobbies: string[]): number {
      // Count the number of common hobbies
      const commonHobbies = loggedInHobbies.filter(hobby => userHobbies.includes(hobby));
      return commonHobbies.length; // Return the number of common hobbies as the similarity score
    },
    getAge(date_of_birth: string) {
      const today = new Date();
      const birthDate = new Date(date_of_birth);
      let age = today.getFullYear() - birthDate.getFullYear();
      const m = today.getMonth() - birthDate.getMonth();
      if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) {
        age--;
      }
      return age;
    },

    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
      }
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    },
    isFriend(friend_id: number): boolean {
      const storeFriendships = useFriendshipsStore();
      const friendships = storeFriendships.friendships;

      return friendships.some((friendship) => 
        (friendship.friend === this.user_id && friendship.user === friend_id) || (this.user_id === friend_id)
      );
    },
    async addFriendship(friend_id: number) {
        const payload = {
          user_id: friend_id,
          friend_id: this.user_id,
          accepted: false,
        };
        console.log(payload);

        const friendshipResponse = await fetch(`http://localhost:8000/friendships/`, 
        {
          method: "POST",
          headers: {
            'Authorization': `Bearer ${VueCookies.get('access_token')}`,
            'Content-Type': 'application/json',
            'X-CSRFToken': VueCookies.get('csrftoken'),
          },
          credentials: 'include',
          body: JSON.stringify(payload),
        });

        // Add the newly created friendship to Pinia store 
        const data = await friendshipResponse.json();
        let createdFriendship = data.friendship as Friendship;

        const friendshipsStore = useFriendshipsStore();
        friendshipsStore.addFriendship(createdFriendship);

        window.location.reload();
        alert(`Friendship requested successfully!`);
      },
    },
    setup() {
          const chosensStore = useChosensStore();
          return { chosensStore};
      },
  },
    
         


);
</script>

<style scoped>
    table, th, td {
    border: 1px solid;
  }


</style>