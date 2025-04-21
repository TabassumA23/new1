import { defineStore } from 'pinia';
import { Allergy } from '../types';

// Cuisines Store
export const useAllergysStore = defineStore('allergys', {
    state: (): {allergys: Allergy[]} => ({
        allergys: [] as Allergy[], // Holds an array of hobbiess
    }),
    getters: {
        // Example getter: find a restaurant by ID
        getAllergyById: (state) => (id: number) => {
            return state.allergys.find(allergy => allergy.id === id);
        },
        getAllergyByName: (state) => (name: string) => {
            return state.allergys.find(allergy => allergy.name === name);
        },
    },
    actions: {
        // Save the list of hobbies
        saveAllergys(allergys: Allergy[]) {
            this.allergys = allergys
        },

        // Add a new Cuisine
        addAllergy(allergy: Allergy) {
            this.allergys.push(allergy);
        },

        // Remove a Cuisine by ID
        removeAllergy(id: number) {
            this.allergys = this.allergys.filter(allergy => allergy.id !== id);
        },
    },
});