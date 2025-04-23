// Vue Router

import { createRouter, createWebHistory } from 'vue-router'

// 1. Define route components.
// These can be imported from other files

import ProfilePage from "../pages/ProfilePage.vue";
import FindFriends from "../pages/FindFriends.vue";
import Reviews from "../pages/Reviews.vue";
import Reservations from "../pages/Reservations.vue";
import Restaurants from "../pages/Restaurants.vue";
import Confirms from "../pages/Confirms.vue";
import Wishlists from "../pages/Wishlists.vue";
import WishlistItems from "../pages/WishlistItems.vue";

let base = (import.meta.env.MODE == 'development') ? import.meta.env.BASE_URL : ''

const router = createRouter({
    history: createWebHistory(base),
    routes:[
  {
    path: "/",
    name: "Profile Page",
    component: ProfilePage,
  },
  {
    path: "/findFriends",
    name: "Find Friends",
    component: FindFriends,
  },
  {
    path: "/confirms",
    name: "Confirms",
    component: Confirms,
  },
  {
    path: "/restaurants",
    name: "Restaurants",
    component: Restaurants,
  },
  {
    path: "/wishlistItems",
    name: "WishlistItems",
    component: WishlistItems,
  },
  {
    path: "/reviews",
    name: "Reviews",
    component: Reviews,
  },
  {
    path: "/reservations",
    name: "Reservations",
    component: Reservations,
  },
  {
    path: "/wishlists",
    name: "Wishlists",
    component: Wishlists,
  },
]
})

export default router;
