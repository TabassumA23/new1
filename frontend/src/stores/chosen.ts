import { defineStore } from "pinia";
import { Chosen } from "../types";

export const usechosenStore = defineStore("chosen", {
  state: (): {chosen: Chosen } => ({
    
    chosen: {} as Chosen, // Holds the currently selected chosen

  }),
 
  actions: {
    // Save the list of chosens
    savechosens(chosen: Chosen) {
      this.chosen = chosen;
    },


    // Fetch a single chosen by ID from the backend
    async fetchChosen(chosenId: number) {
      try {
        const response = await fetch(`http://localhost:8000/chosen/${chosenId}/`);
  
        if (!response.ok) {
          throw new Error("Failed to fetch chosen data");
        }
        const chosenData = await response.json();
        this.chosen = chosenData; // Update the state with the fetched chosen data
      
      } catch (error) {
        console.error("Error fetching chosen data:", error);
      }
    },

    
  },
});