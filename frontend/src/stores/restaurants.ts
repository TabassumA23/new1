import { defineStore } from 'pinia';
import { Restaurant } from '../types';

// restaurants Store
export const useRestaurantsStore = defineStore('restaurants', {
    state: (): {restaurants: Restaurant[]} => ({
        restaurants: [] as Restaurant[], // Holds an array of hobbiess
    }),
    getters: {
        // Example getter: find a restaurant by ID
        getRestaurantById: (state) => (id: number) => {
            return state.restaurants.find(restaurant => restaurant.id === id);
        },
        getRestaurantByName: (state) => (name: string) => {
            return state.restaurants.find(restaurant => restaurant.name === name);
        },
    },
    actions: {
        // Save the list of hobbies
        saveRestaurants(restaurants: Restaurant[]) {
            this.restaurants = restaurants
        },

        // Add a new restaurant
        addRestaurant(restaurant: Restaurant) {
            this.restaurants.push(restaurant);
        },

        // Remove a restaurant by ID
        removeRestaurant(id: number) {
            this.restaurants = this.restaurants.filter(restaurant => restaurant.id !== id);
        },
    },
});