import { defineStore } from 'pinia'
import { ChosenAllergy } from '../types'

export const useChosenAllergysStore = defineStore('chosenAllergys', {
    state: () => ({ 
        chosenAllergys: [] as ChosenAllergy[],
    }),
    getters: {
        getChosenallergyByName: (state) => (name: string) => {
            return state.chosenAllergys.find(chosenAllergy => chosenAllergy.name === name);
        },
    },
    actions: {
        saveChosenAllergys(chosenAllergys: ChosenAllergy[]) {
            this.chosenAllergys = chosenAllergys
        },
        // Add a new chosenAllergy 
        addChosen(chosenAllergy: ChosenAllergy) {
            this.chosenAllergys.push(chosenAllergy);
        },
        removeChosenallergy(chosenAllergyId: number) {
            this.chosenAllergys = this.chosenAllergys.filter((f) => f.id !== chosenAllergyId);
        }
    }
})