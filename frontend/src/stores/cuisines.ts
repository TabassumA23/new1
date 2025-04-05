import { defineStore } from 'pinia';
import { Cuisine } from '../types';

// Cuisines Store
export const useCuisinesStore = defineStore('cuisines', {
    state: (): {cuisines: Cuisine[]} => ({
        cuisines: [] as Cuisine[], // Holds an array of hobbiess
    }),
    getters: {
        // Example getter: find a restaurant by ID
        getCuisineById: (state) => (id: number) => {
            return state.cuisines.find(cuisine => cuisine.id === id);
        },
        getCuisineByName: (state) => (name: string) => {
            return state.cuisines.find(cuisine => cuisine.name === name);
        },
    },
    actions: {
        // Save the list of hobbies
        saveCuisines(cuisines: Cuisine[]) {
            this.cuisines = cuisines
        },

        // Add a new Cuisine
        addCuisine(cuisine: Cuisine) {
            this.cuisines.push(cuisine);
        },

        // Remove a Cuisine by ID
        removeCuisine(id: number) {
            this.cuisines = this.cuisines.filter(cuisine => cuisine.id !== id);
        },
    },
});