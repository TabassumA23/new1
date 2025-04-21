import { defineStore } from "pinia";
import { ChosenAllergy } from "../types";

export const usechosenAllergyStore = defineStore("chosenAllergy", {
  state: (): {chosenAllergy: ChosenAllergy } => ({
    
    chosenAllergy: {} as ChosenAllergy, // Holds the currently selected chosenAllergy

  }),
 
  actions: {
    // Save the list of chosenAllergys
    saveChosenAllergys(chosenAllergy: ChosenAllergy) {
      this.chosenAllergy = chosenAllergy;
    },


    // Fetch a single chosenAllergy by ID from the backend
    async fetchChosenAllergy(chosenAllergyId: number) {
      try {
        const response = await fetch(`http://localhost:8000/chosenAllergy/${chosenAllergyId}/`);
  
        if (!response.ok) {
          throw new Error("Failed to fetch chosenAllergy data");
        }
        const chosenAllergyData = await response.json();
        this.chosenAllergy = chosenAllergyData; // Update the state with the fetched chosenAllergy data
      
      } catch (error) {
        console.error("Error fetching chosenAllergy data:", error);
      }
    },

    
  },
});