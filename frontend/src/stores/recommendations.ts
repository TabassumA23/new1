import { defineStore } from 'pinia'
import { Restaurant } from '../types';

export const useRecommendationsStore = defineStore('recommendations', {
  state: () => ({
    restaurants: [] as Restaurant[],
  }),
  actions: {
    set(newList: Restaurant[]) {
      this.restaurants = newList
    }
  }
})
