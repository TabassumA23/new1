import { defineStore } from 'pinia'
import { ChosenCuisine } from '../types'

export const useChosenCuisinesStore = defineStore('chosenCuisines', {
    state: () => ({ 
        chosenCuisines: [] as ChosenCuisine[],
    }),
    getters: {
        getChosencuisineByName: (state) => (name: string) => {
            return state.chosenCuisines.find(chosenCuisine => chosenCuisine.name === name);
        },
    },
    actions: {
        saveChosenCuisines(chosenCuisines: ChosenCuisine[]) {
            this.chosenCuisines = chosenCuisines
        },
        // Add a new chosencuisine hobby
        addChosen(chosenCuisine: ChosenCuisine) {
            this.chosenCuisines.push(chosenCuisine);
        },
        removeChosencuisine(chosenCuisineId: number) {
            this.chosenCuisines = this.chosenCuisines.filter((f) => f.id !== chosenCuisineId);
        }
    }
})