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

                      <!-- Go to reviews page -->
                    <router-link
                        class="link"
                        :to="{name: 'Reviews'}"
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
    main{
        background-color:rgb(234, 91, 91);
        font-family: Arial, Helvetica, sans-serif;
    }
    
    .navbar{
        display: flex;
        background-color:rgb(234, 91, 91);
        padding-left: 0.5rem
    }

    .nav-parts{
        display:flex;
    }

    .nav-parts > .link, a{
        padding: 0.5em;
        text-decoration: none;
        margin: 1em;
        color: black;
        font-size: 1rem;
        background-color:rgb(234, 91, 91);
        border: none;
    }
</style>
