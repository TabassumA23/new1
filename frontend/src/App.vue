<template>
    <main>
        <!--Nav bar for every page -->
        <div class="navbar">
       
                <h2>HobbyMate</h2>
                <div class="nav-parts">
                      <!--Go to home page / profile page-->
                    <router-link
                        class="link"
                        :to="{name: 'Profile Page'}"
                    >
                        Home
                    </router-link>
                      <!-- Go to find friends-->
                    <router-link
                        class="link"
                        :to="{name: 'Find Friends'}"
                    >
                        Find A Friend
                    </router-link>
                    <router-link
                        class="link"
                        :to="{name: 'Restaurants'}"
                    >
                      
                        Reviews
                    </router-link>
                    <!-- reservations page-->
                    <router-link
                        class="link"
                        :to="{name: 'Reservations'}"
                    >
                        Reservations
                    </router-link>

                    <!-- Logout -->
                    <a href= 'http://localhost:8000/logout/'>Log Out</a>
                </div>
        </div>
        <RouterView class="flex-shrink-0" />
    </main>

</template>

<script lang="ts">
import { defineComponent } from "vue";
import { RouterView } from "vue-router";

export default defineComponent({
    components: { RouterView },
});

</script>
  <!--Styling for page and navbar mainly colour and positions-->
<style scoped>
    main {
        background-color: #F0F8FF; 
        font-family: Arial, Helvetica, sans-serif;
        padding: 2rem;
    }

    .navbar {
        display: flex;
        justify-content: space-between;
        background-color: #4F97C6; 
        padding: 1rem;
        border-radius: 10px;
    }

    .nav-parts {
        display: flex;
        align-items: center;
    }

    .nav-parts > .link,
    a {
        padding: 0.7em;
        text-decoration: none;
        color: white;
        font-size: 1.1rem;
        background-color: #1D5673; 
        border-radius: 5px;
        margin-right: 1rem;
        transition: background-color 0.3s ease;
    }

    .nav-parts > .link:hover,
    a:hover {
        background-color: #B5D3E7; 
    }

    .navbar h1 {
        color: #1D5673;
        font-size: 2rem;
    }

    .main-content {
        padding: 2rem;
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    button {
        padding: 0.8rem 2rem;
        background-color: #4F97C6; 
        color: white;
        font-size: 1rem;
        border-radius: 5px;
        border: none;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }

    button:hover {
        background-color: #1D5673; 
    }

    input, textarea {
        padding: 1rem;
        width: 100%;
        border: 1px solid #B5D3E7; 
        border-radius: 5px;
        font-size: 1rem;
        margin-bottom: 1rem;
    }

    h3 {
        color: #1D5673; 
        font-size: 1.4rem;
        margin-bottom: 1rem;
    }

   
    
</style>

