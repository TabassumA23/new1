import { defineStore } from 'pinia'
import { Chosen } from '../types'

export const useChosensStore = defineStore('chosens', {
    state: () => ({ 
        chosens: [] as Chosen[],
    }),
    getters: {
        getChosenByName: (state) => (name: string) => {
            return state.chosens.find(chosen => chosen.name === name);
        },
    },
    actions: {
        saveChosens(chosens: Chosen[]) {
            this.chosens = chosens
        },
        // Add a new chosen hobby
        addChosen(chosen: Chosen) {
            this.chosens.push(chosen);
        },
        removeChosen(chosenId: number) {
            this.chosens = this.chosens.filter((f) => f.id !== chosenId);
        }
    }
})