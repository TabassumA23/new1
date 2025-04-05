import { defineStore } from "pinia";
import { ChosenCuisine } from "../types";

export const usechosenCuisineStore = defineStore("chosenCuisine", {
  state: (): {chosenCuisine: ChosenCuisine } => ({
    
    chosenCuisine: {} as ChosenCuisine, // Holds the currently selected chosenCuisine

  }),
 
  actions: {
    // Save the list of chosenCuisines
    saveChosenCuisines(chosenCuisine: ChosenCuisine) {
      this.chosenCuisine = chosenCuisine;
    },


    // Fetch a single chosenCuisine by ID from the backend
    async fetchChosenCuisine(chosenCuisineId: number) {
      try {
        const response = await fetch(`http://localhost:8000/chosenCuisine/${chosenCuisineId}/`);
  
        if (!response.ok) {
          throw new Error("Failed to fetch chosenCuisine data");
        }
        const chosenCuisineData = await response.json();
        this.chosenCuisine = chosenCuisineData; // Update the state with the fetched chosenCuisine data
      
      } catch (error) {
        console.error("Error fetching chosenCuisine data:", error);
      }
    },

    
  },
});