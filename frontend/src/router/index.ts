// Vue Router

import { createRouter, createWebHistory } from 'vue-router'

// 1. Define route components.
// These can be imported from other files

import ProfilePage from "../pages/ProfilePage.vue";
import FindFriends from "../pages/FindFriends.vue";
import Reviews from "../pages/Reviews.vue";

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
    path: "/reviews",
    name: "Reviews",
    component: Reviews,
  },
]
})

export default router;
